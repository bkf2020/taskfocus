setInterval(() => {
    chrome.runtime.sendMessage({ type: "ping" }, (response) => {
		console.log(response);
	});
}, 5000);