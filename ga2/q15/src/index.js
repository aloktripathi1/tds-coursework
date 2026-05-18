export default {
    async fetch(request, env, ctx) {
        // Handle CORS preflight
        if (request.method === "OPTIONS") {
            return new Response(null, {
                status: 204,
                headers: corsHeaders(),
            });
        }

        const url = new URL(request.url);

        // POST /data endpoint
        if (request.method === "POST" && url.pathname === "/data") {
            try {
                const body = await request.json();
                const { type, value } = body;
                let reversed;

                switch (type) {
                    case "string":
                        reversed = value.split("").reverse().join("");
                        break;
                    case "array":
                        reversed = [...value].reverse();
                        break;
                    case "words":
                        reversed = value.split(/\s+/).reverse().join(" ");
                        break;
                    case "number":
                        const isNegative = value < 0;
                        const absStr = Math.abs(value).toString();
                        const reversedStr = absStr.split("").reverse().join("");
                        reversed = parseInt(reversedStr, 10) * (isNegative ? -1 : 1);
                        break;
                    default:
                        return jsonResponse({ error: `Unknown type: ${type}` }, 400);
                }

                return jsonResponse({
                    reversed,
                    email: "your-student-id",
                });
            } catch (err) {
                return jsonResponse({ error: "Invalid JSON body" }, 400);
            }
        }

        // Fallback
        return jsonResponse(
            { message: "POST to /data with { type, value }" },
            404
        );
    },
};

function corsHeaders() {
    return {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type",
    };
}

function jsonResponse(data, status = 200) {
    return new Response(JSON.stringify(data), {
        status,
        headers: {
            "Content-Type": "application/json",
            ...corsHeaders(),
        },
    });
}
