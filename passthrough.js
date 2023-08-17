// Do not decode anything, just put it into as is
var bytes = convertToUint8Array([]);
var port = 10;
var arr = [];
for (var i = 0; i < bytes.length; i++) {
	arr.push(bytes[i]);
}
return {"bytes": JSON.stringify(arr), "port": port, "payload length": bytes.length};