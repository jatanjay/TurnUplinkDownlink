let payload = "MDAwMDAwMDAxYjUyNzQwMjE2NTQzMzRhNGQ0ZDU2MDMzMDMwMzkzMTQ1NDIzMjM5MzkzNzM2MzM0MjAwMDAwMA==";
let decoded = atob(payload);

function converthextostring(hex) {
    var str = '';
    for (var i = 0; i < hex.length; i += 2) {
        str += String.fromCharCode(parseInt(hex.substr(i, 2), 16));
    }
    return str;
}


let hex_bytes = converthextostring(decoded);

