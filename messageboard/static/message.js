let img = null;
let message = null;
let form = document.querySelector(".form__content");
// let myPic = document.querySelector(".myPic");
let selectedFile = document.querySelector(".form__picFile");
let clientText = document.querySelector(".form__messageText");

function buildDatabaseMessageboard(dbContentArray, dbMessageQty) {
	let divDB = document.createElement("div");
	document.body.appendChild(divDB);
	divDB.id = "messageDB__outer";
	let dbMessage = [];
	let dbPic = [];
	for (data in dbContentArray) {
		let message = dbContentArray[data].word;
		let img = dbContentArray[data].image;
		dbMessage.push(message);
		dbPic.push(img);
	}
	for (item = 0; item < dbMessageQty; item++) {
		//抓取每個點的info
		let perMessage = dbMessage[item];
		let perPic = dbPic[item];
		let diveDBInner = document.createElement("div");
		diveDBInner.id = "messageDB__inner";
		divDB.appendChild(diveDBInner);
		let messageBox = document.createElement("div");
		messageBox.id = "messageDB__messageBox";
		diveDBInner.appendChild(messageBox);
		messageBox.innerHTML = perMessage;
		let imgBox = document.createElement("img");
		imgBox.id = "messageDB__imgBox";
		imgBox.src = perPic;
		diveDBInner.appendChild(imgBox);
		let line = document.createElement("hr");
		diveDBInner.appendChild(line);
	}
}

async function loadMessageboard() {
	let url = `file/load`;
	let fetchInfo = await fetch(url, {
		method: "GET",
	});
	dbContent = await fetchInfo.json();
	dbContentArray = dbContent.data;
	dbMessageQty = dbContent.count;
	buildDatabaseMessageboard(dbContentArray, dbMessageQty);
}
loadMessageboard();

async function getContent() {
	let url = `file/upload`;
	let fetchInfo = await fetch(url, {
		method: "GET",
	});
	messageContent = await fetchInfo.json();
	img = messageContent["data"]["image"];
	message = messageContent["data"]["word"];
}
function buildMessageboard() {
	let div = document.createElement("div");
	document.body.appendChild(div);
	div.id = "message__outer";
	let messageBox = document.createElement("div");
	messageBox.id = "message__messageBox";
	div.appendChild(messageBox);
	messageBox.innerHTML = message;
	let imgBox = document.createElement("img");
	imgBox.id = "message__imgBox";
	imgBox.src = img;
	div.appendChild(imgBox);
	let line = document.createElement("hr");
	div.appendChild(line);
}

async function uploadContent(event) {
	event.preventDefault();
	let formData = new FormData(form);
	let file = selectedFile.files[0];
	let fileName = file.name;
	let clientMessage = clientText.value;
	formData.append("fileName", fileName);
	formData.append("file", file);
	formData.append("message", clientMessage);
	let url = `file/upload`;
	await fetch(url, {
		method: "POST",
		body: formData,
	});
	await getContent();
	buildMessageboard();
}

form.addEventListener("submit", uploadContent);
