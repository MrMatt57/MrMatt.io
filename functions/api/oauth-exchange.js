var ALLOWED_ORIGIN = 'https://mrmatt.io';

function corsHeaders(request) {
    var origin = request.headers.get('Origin') || '';
    // Only allow our own domain
    var allowedOrigin = origin === ALLOWED_ORIGIN ? ALLOWED_ORIGIN : '';
    return {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': allowedOrigin,
        'Access-Control-Allow-Methods': 'POST',
        'Access-Control-Allow-Headers': 'Content-Type'
    };
}

export async function onRequestPost(context) {
    var request = context.request;
    var env = context.env;
    var headers = corsHeaders(request);

    try {
        var body = await request.json();
        var code = body.code;
        var state = body.state;

        if (!code) {
            return new Response(JSON.stringify({ error: 'Missing code parameter' }), {
                status: 400, headers: headers
            });
        }

        var clientId = env.GITHUB_CLIENT_ID;
        var clientSecret = env.GITHUB_CLIENT_SECRET;

        if (!clientId || !clientSecret) {
            return new Response(JSON.stringify({ error: 'OAuth not configured' }), {
                status: 500, headers: headers
            });
        }

        var tokenResponse = await fetch('https://github.com/login/oauth/access_token', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify({
                client_id: clientId,
                client_secret: clientSecret,
                code: code
            })
        });

        var tokenData = await tokenResponse.json();

        if (tokenData.error) {
            return new Response(JSON.stringify({ error: tokenData.error_description || tokenData.error }), {
                status: 400, headers: headers
            });
        }

        return new Response(JSON.stringify({ token: tokenData.access_token }), {
            status: 200, headers: headers
        });
    } catch (err) {
        return new Response(JSON.stringify({ error: 'Internal server error' }), {
            status: 500, headers: headers
        });
    }
}

export async function onRequestOptions(context) {
    var headers = corsHeaders(context.request);
    headers['Content-Type'] = '';
    return new Response(null, { status: 204, headers: headers });
}
