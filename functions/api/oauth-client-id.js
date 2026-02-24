export async function onRequestGet(context) {
    var clientId = context.env.GITHUB_CLIENT_ID;

    if (!clientId) {
        return new Response(JSON.stringify({ error: 'OAuth not configured' }), {
            status: 500,
            headers: { 'Content-Type': 'application/json' }
        });
    }

    return new Response(JSON.stringify({ client_id: clientId }), {
        status: 200,
        headers: { 'Content-Type': 'application/json' }
    });
}
