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

function displayWebsitesBlocked() {
	var userRulesList = document.getElementById("blockedWebsites");
	while(userRulesList.firstChild) {
		userRulesList.removeChild(userRulesList.firstChild);
	}
    chrome.storage.sync.get(['userRules'], function(result) {
        if(result.userRules === undefined) return false;
        for(var i = 0; i < result.userRules.length; i++) {
            var item = document.createElement("li");
			item.innerText = result.userRules[i];
			userRulesList.appendChild(item);
        }
        return true;
    });
    chrome.storage.sync.get(['rules_json'], function(result) {
        if(result.rules_json === undefined) return false;
        console.log(result.rules_json);
        return true;
    });
    chrome.storage.sync.get(['whitelist'], function(result) {
        if(result.whitelist === undefined) return false;
        console.log(result.whitelist);
        return true;
    });
}

displayWebsitesBlocked();