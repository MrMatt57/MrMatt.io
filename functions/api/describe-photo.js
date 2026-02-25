var ALLOWED_ORIGIN = 'https://mrmatt.io';

var SYSTEM_PROMPT = [
    'You are writing photo descriptions for a personal photography gallery.',
    '',
    'For the given photo, respond with ONLY valid JSON (no markdown, no code fences):',
    '{',
    '  "title": "Short title, 2-4 words",',
    '  "alt": "One factual sentence describing what is visible, for screen readers",',
    '  "description": "1-2 natural sentences describing the photo. Match the tone to the subject matter. Don\'t force connections to hobbies or interests unless clearly relevant."',
    '}'
].join('\n');

function corsHeaders(request) {
    var origin = request.headers.get('Origin') || '';
    var allowedOrigin = origin === ALLOWED_ORIGIN ? ALLOWED_ORIGIN : '';
    return {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': allowedOrigin,
        'Access-Control-Allow-Methods': 'POST',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization'
    };
}

export async function onRequestPost(context) {
    var request = context.request;
    var env = context.env;
    var headers = corsHeaders(request);

    try {
        var apiKey = env.ANTHROPIC_API_KEY;
        if (!apiKey) {
            return new Response(JSON.stringify({ error: 'AI descriptions not configured' }), {
                status: 500, headers: headers
            });
        }

        var body = await request.json();
        var imageBase64 = body.image;
        var mediaType = body.media_type || 'image/jpeg';
        var feedback = body.feedback || '';

        if (!imageBase64) {
            return new Response(JSON.stringify({ error: 'Missing image data' }), {
                status: 400, headers: headers
            });
        }

        var userText = 'Describe this photo for my gallery.';
        if (feedback) {
            userText += ' Additional direction from the photographer: ' + feedback;
        }

        var anthropicResponse = await fetch('https://api.anthropic.com/v1/messages', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'x-api-key': apiKey,
                'anthropic-version': '2023-06-01'
            },
            body: JSON.stringify({
                model: 'claude-haiku-4-5-20251001',
                max_tokens: 300,
                system: SYSTEM_PROMPT,
                messages: [{
                    role: 'user',
                    content: [
                        {
                            type: 'image',
                            source: {
                                type: 'base64',
                                media_type: mediaType,
                                data: imageBase64
                            }
                        },
                        {
                            type: 'text',
                            text: userText
                        }
                    ]
                }]
            })
        });

        if (!anthropicResponse.ok) {
            var errText = await anthropicResponse.text();
            return new Response(JSON.stringify({ error: 'AI API error: ' + anthropicResponse.status }), {
                status: 502, headers: headers
            });
        }

        var aiData = await anthropicResponse.json();
        var text = aiData.content && aiData.content[0] && aiData.content[0].text;

        if (!text) {
            return new Response(JSON.stringify({ error: 'Empty AI response' }), {
                status: 502, headers: headers
            });
        }

        // Parse JSON from response (handle possible markdown fences)
        var jsonStr = text.replace(/^```json?\s*/, '').replace(/\s*```$/, '').trim();
        var result = JSON.parse(jsonStr);

        return new Response(JSON.stringify(result), {
            status: 200, headers: headers
        });
    } catch (err) {
        return new Response(JSON.stringify({ error: 'Failed to describe photo: ' + err.message }), {
            status: 500, headers: headers
        });
    }
}

export async function onRequestOptions(context) {
    var headers = corsHeaders(context.request);
    headers['Content-Type'] = '';
    return new Response(null, { status: 204, headers: headers });
}
