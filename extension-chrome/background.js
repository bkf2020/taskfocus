/*
    liblock: libre site blocker to block distracting websites
    Copyright (C) 2021-present bkf2020

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, ONLY version 3 of the License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
*/

chrome.alarms.create({ periodInMinutes: 1 });
chrome.alarms.onAlarm.addListener(
	async function updateRules() {
		chrome.storage.sync.get(['userRules'], async function(result) {
			if(result.userRules === undefined) return false;
			var rules_id = [];
			var ids = "";
			for(var i = 1; i <= result.userRules.length; i++) {
				rules_id.push(i);
			}
			rules_id.push(10000);
			chrome.declarativeNetRequest.updateDynamicRules({"removeRuleIds": rules_id});
			var oldRules = await chrome.declarativeNetRequest.getDynamicRules();
			console.log(oldRules);
			return true;
		});

		var rules = [];
		var whitelist = [];
		try {
			const tasks = await fetch("http://localhost:8000/tasks/json/");
			const tasksData = await tasks.json();
			for(var idx in tasksData) {
				if(tasksData[idx]["start_time"] * 1000 <= Date.now() && Date.now() <= tasksData[idx]["end_time"] * 1000) {
					for (var i = 0; i < tasksData[idx]["websites"].length; i++) {
						whitelist.push(tasksData[idx]["whitelist"]);
						rules.push(tasksData[idx]["websites"][i]);
					}
				}
			}
		} catch (error) {
			console.error("Error:", error);
		}

		if(whitelist.length > 0 && whitelist[0]) {
			rules.push("localhost");
			whitelist.push(true);
		}

		var rules_json = [];
		var curr_id = 1;
		var first = false;
		for(var i = 0; i < rules.length; i++) {
			var r = rules[i];
			if(r !== "") {
				if(!whitelist[i]) {
					rules_json.push({
						"id": curr_id,
						"priority": 1,
						"action": { "type": "redirect", "redirect": { "extensionPath": "/blocked.html" } },
						"condition": {
							"urlFilter": "||" + r,
							"resourceTypes": [
								"main_frame",
								"sub_frame"
							]
						}
					});
					curr_id++;
				} else {
					rules_json.push({
						"id": curr_id,
						"priority": 1,
						"action": { "type": "allow" },
						"condition": {
							"urlFilter": "||" + r,
							"resourceTypes": [
								"main_frame",
								"sub_frame"
							]
						}
					});
					curr_id++;
				}
			}
		}
		if(whitelist.length > 0 && whitelist[0]) {
			rules_json.push({
				"id": 10000,
				"priority": 1,
				"action": { "type": "block" },
				"condition": {
					"urlFilter": '*',
					"resourceTypes": [
						"main_frame",
						"sub_frame"
					]
				}
			});
		}

		if (rules_json.length > 0) {
			chrome.declarativeNetRequest.updateDynamicRules({"addRules": rules_json});
		}
		chrome.storage.sync.set({rules_json: rules_json});
		chrome.storage.sync.set({whitelist: whitelist});

		// close tabs that are on the blocklist
		var rules_url_pattern = [];
		for(var i = 0; i < rules.length; i++) {
			var r = rules[i];
			if(r !== "") {
				// format (e.g. for google.com): *://*.google.com/*
				rules_url_pattern.push("*://*." + r + "/*");
			}
		}
		if(whitelist[0]) {
			var acceptedTabIds = [];
			chrome.tabs.query({"url" : rules_url_pattern}).then(function(result2) {
				for(var i = 0; i < result2.length; i++) {
					acceptedTabIds.push(result2[i].id);
				}
			});
			console.log(acceptedTabIds);
			chrome.tabs.query({"url" : "*://*/*"}).then(function(result) {
				for(var i = 0; i < result.length; i++) {
					var tabId = result[i].id;
					console.log(acceptedTabIds.includes(tabId));
					if(!acceptedTabIds.includes(tabId)) {
						chrome.tabs.remove(tabId);
					}
				}
			});
		} else if(rules_url_pattern.length > 0) {
			chrome.tabs.query({"url" : rules_url_pattern}).then(function(result) {
				for(var i = 0; i < result.length; i++) {
					var tab = result[i];
					chrome.tabs.remove(tab.id);
				}
			});
		}

		var rules_not_empty = [];
		for(var i = 0; i < rules.length; i++) {
			var r = rules[i];
			if(r !== "") {
				rules_not_empty.push(r);
			}
		}

		chrome.storage.sync.set({userRules: rules_not_empty});
	}
);