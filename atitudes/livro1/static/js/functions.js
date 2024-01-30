 document.addEventListener("keyup", function (e) {
    var keyCode = e.keyCode ? e.keyCode : e.which;
            if (keyCode == 44) {
                stopPrntScr();
            }
        });
function stopPrntScr() {

            var inpFld = document.createElement("input");
            inpFld.setAttribute("value", ".");
            inpFld.setAttribute("width", "0");
            inpFld.style.height = "0px";
            inpFld.style.width = "0px";
            inpFld.style.border = "0px";
            document.body.appendChild(inpFld);
            inpFld.select();
            document.execCommand("copy");
            inpFld.remove(inpFld);
        }
       function AccessClipboardData() {
            try {
                window.clipboardData.setData('text', "Access   Restricted");
            } catch (err) {
            }
        }
        setInterval("AccessClipboardData()", 300);

function thunkableMessage(tMessage){
    ThunkableWebviewerExtension.postMessage(tMessage);
}

function rollDice(){
	var value_dice, number;
	value_dice = "dice fas fa-dice"
	number = Math.floor(Math.random() * 6)+1;
    switch (number) {
      case 1:
        value_dice += "-one";
        break;
      case 2:
        value_dice += "-two";
        break;
      case 3:
        value_dice += "-three";
        break;
      case 4:
        value_dice += "-four";
        break;
      case 5:
        value_dice += "-five";
        break;
      case  6:
        value_dice += "-six";
	}
    document.getElementById("dice").className = value_dice;
}

function openSide(side,btn) {
  aside = document.getElementById(side);
  if (aside.style.width == "400px"){
  	aside.style.width = "0px";
    aside.style.padding = "0px";
  }else {
  	aside.style.width = "400px";
    aside.style.padding = "20px";
  }
  bside = document.getElementById(btn);
  bside.classList.toggle("change");
}
function justOpenSide(side,btn){
  aside = document.getElementById(side);
  if (aside.style.width != "400px"){
	aside.style.width = "400px";
    aside.style.padding = "20px";
    bside = document.getElementById(btn);
  	bside.classList.toggle("change");
  }
}
function closeSide(side, btn){
  aside = document.getElementById(side);
  if (aside.style.width != "0px"){
  	aside.style.width = "0px";
    aside.style.padding = "0px";
    bside = document.getElementById(btn);
  	bside.classList.toggle("change");
  }
}

function openMenu(menu){
  menu = document.getElementById(menu);
  if (menu.style.height == "300px"){
    menu.style.height = "0px";
  } else {
    menu.style.height = "300px";
  }
}

function screenSize(){
    x = window.innerWidth;
    if (x > 1499) {
	    openSide('rightSide', 'rightBtn');
    }
    if (x > 999) {
        openSide('leftSide', 'leftBtn');
    }
}

function openPage(open, close){
    var p_open = document.getElementById(open);
    var p_close = document.getElementById(close);
    p_open.style.height = "100%";
    p_close.style.height = "0px";
    p_open.scrollIntoView();
}

function showAuthor(authorID){
    var author = document.getElementById(authorID);
    author.style.opacity = 100;
}

function openImage(img) {
	var modal = document.getElementById("imageModal");
    var modalImg = document.getElementById("bigImage");
    var captionText = document.getElementById("caption");

    modal.style.display = "block";
    modalImg.src = img.src;
    captionText.innerHTML = img.alt;
}

function closeModal(modal) { 
	var modal = document.getElementById(modal);
  	modal.style.display = "none";
}

function showModal(modalID){
	var modal = document.getElementById(modalID);
	modal.style.display = "block";
}

function hideOrShow(id, action){
	var item = document.getElementById(id);
	if (action == 0){
		item.style.display = "none";
	}else {
		item.style.display = "block";
	}
}

function changeFont(getID,setID){
	var value = document.getElementById(getID).value;
	var setFont = document.getElementById(setID);
	if (value == "p"){
		setFont.style="font-size: 20px; font-weight: normal; text-align: justify; font-style: normal; font-variant-caps: normal;";
	} else if (value == "em"){
		setFont.style="font-size: 20px; font-weight: bold; text-align: left; font-style: normal; font-variant-caps: normal;";
	} else if (value == "h3"){
		setFont.style="font-size: 25px; font-weight: normal; text-align: left; font-style: italic; font-variant-caps: normal;";
	} else if (value == "strong"){
		setFont.style="font-size: 20px; font-weight: bold; text-align: left; font-style: normal; font-variant-caps: small-caps;";
	} else if (value == "h2"){
		setFont.style="font-size: 28px; font-weight: bold; text-align: left; font-style: normal; font-variant-caps: normal;";
	}
}

function changeColor(getID,setID){
	var value = document.getElementById(getID).value;
	var setColor = document.getElementById(setID);
	if (value == 'pink'){
		setColor.style.color = 'deeppink';
	} else {
		setColor.style.color = value;
	}
}

function editParagraph(pID){
	var p = document.getElementById(pID);
	var delBtn = document.getElementById('deleteBtn');
	var caption = document.getElementById('text_caption');
	var input = document.getElementById('fparagraph_id');
	var paragraph = document.getElementById('fparagraph');
	if (input.value != pID && input.value != ''){
		document.getElementById(input.value).classList.remove("alert");
	}
	if (p.classList.contains("alert")){
		p.classList.remove("alert");
		delBtn.className = 'hide';
		caption.innerHTML = '';
		paragraph.innerHTML = '';
		input.value = '';
	} else {
		p.classList.add("alert");
		delBtn.className = 'alert';
		caption.innerHTML = "Você está EDITANDO um paragrafo";
		paragraph.innerHTML = p.innerHTML;
		input.value = pID;
	}
	caption.scrollIntoView();
} 

function selectAvatar(userID,avatarID,price,breed,name){
	var hidden = document.getElementById("avatar_items");
	if (breed == 0){
		var showAvatar = document.getElementById("background");
		var showPrice = document.getElementById("background_price");
		var otherPrice = document.getElementById("avatar_price");
		var showName = document.getElementById("bg_name");
		hidden.value = avatarID;
	} else {
		var showAvatar = document.getElementById("avatar");
		var showPrice = document.getElementById("avatar_price");
		var otherPrice = document.getElementById("background_price");
		var showName = document.getElementById("av_name");
		hidden.name = avatarID;
	}
    var avatar = document.getElementById(avatarID);
    var totalPrice = document.getElementById("total_price");
    showName.innerHTML = name
    showAvatar.src = avatar.src; 
    showPrice.innerHTML = price;
    totalPrice.innerHTML = Number(price) + Number(otherPrice.innerHTML);
    var btnSave = document.getElementById("btnSave");
    btnSave.href = "/user/setAvatar/"+userID+"/"+hidden.name+"/"+hidden.value+"/"+totalPrice.innerHTML+"/";  
    justOpenSide('leftSide','leftBtn');
}

function resetAvatar(userID){
	var hidden = document.getElementById("avatar_items");
	var showAvatar = document.getElementById("avatar");
	var showBg = document.getElementById("background");
	var avatarName = document.getElementById("bg_name");
	var bgName = document.getElementById("av_name");
    var btnSave = document.getElementById("btnSave");
	var bgPrice = document.getElementById("background_price");
	var avPrice = document.getElementById("avatar_price");
    var totalPrice = document.getElementById("total_price");
    hidden.value = 0;
    hidden.name = 0;
    showBg.src = "/static/img/avatars/0/1.jpg";
    showAvatar.src = "/static/img/avatars/default.jpg";
    avatarName.innerHTML = "Avatar";
    bgName.innerHTML = "Fundo";
    btnSave.href = "/user/setAvatar/"+userID+"/0/0/0/";  
    bgPrice.innerHTML = "0.00";
    avPrice.innerHTML = "0.00";
    totalPrice.innerHTML = "0.00";
}

function selectAnswerAlter(iconID, scoreID, SelectID, others){
	var select = document.getElementById(SelectID);
	var selected = select.options[select.selectedIndex];
	for(var i=0; i<others.length; i++) {
		var other = document.getElementById(others[i]);
		if(other.value == select.value) { 
	        selected.value = 'False';
	        break;
	    }
	}
	if(selected.value.substring(1) == 'False'){
		selected.value = 'False';
	}
	selectAnswer(iconID, scoreID, SelectID);
}
function selectAnswer(iconID, scoreID, SelectID){
	var icon = document.getElementById(iconID);
	var scoreValue = document.getElementById(scoreID);
	var select = document.getElementById(SelectID);
	var value = select.value;
	score = scoreValue.value;
	if (value == "False"){
		if (score == 10){
			scoreValue.value -= 1; 
		} else if(score > 1){
			scoreValue.value -= 2;
		}
		score = scoreValue.value;
	} else if (value == "F"){ 
		if (score == 10){
			scoreValue.value -= 1; 
		} else if(score > 1){
			scoreValue.value -= 2;
		}
		score = scoreValue.value;
		select.style="background-color: #00008B; color: white;";
		select.disabled = true;
		icon.style="color: orange;"
		var hits = document.getElementById("hits");
		var totalScore = document.getElementById("totalScore");
		hits.innerHTML = Number(hits.innerHTML) + 1;
		totalScore.innerHTML = Number(totalScore.innerHTML) + Number(score);
	} else {
		select.style="background-color: #00008B; color: white;";
		select.disabled = true;
		icon.style="color: orange;"
		var hits = document.getElementById("hits");
		var totalScore = document.getElementById("totalScore");
		hits.innerHTML = Number(hits.innerHTML) + 1;
		totalScore.innerHTML = Number(totalScore.innerHTML) + Number(score); 
	}
	switch (Number(score)) {
	  case 1:
		icon.className = "fas fa-frown";
		break;
	  case 3:
		icon.className = "fas fa-meh";
		break;
	  case 5:
		icon.className = "fas fa-smile";
		break;
	  case 7:
		icon.className = "fas fa-grin-alt";
	}
}

function questFinish(modal,questNumber,lesson,page,target) {
	var hits = document.getElementById("hits");
	var hit = target/10;
	if (Number(hits.innerHTML) < hit){
		alert('Você ainda não acertou todas as respostas');
	} else {
		var totalScore = document.getElementById("totalScore");
		score = totalScore.innerHTML;
		var questCaption = document.getElementById("questCaption");
		var reward = document.getElementById("reward");
		if (score == target){
			questCaption.innerHTML = 'Você fez a pontuação máxima.';
		} else if (score >= target/2){
			questCaption.innerHTML = 'Você foi bem, mas poderia ir melhor.';
		} else if (score >= 0){
			questCaption.innerHTML = 'Você fez poucos pontos, mas pode tentar de novo.';
		} else {
			questCaption.innerHTML = 'Você marcou uma pontuação negativa, Você receberá 0 pontos';
			score = 0;
		}
		reward.innerHTML = 'Você ganhou: '+ score +' pontos, '+ score +' créditos e um troféu joinha';
		document.getElementById("conclud").href = '/questConclude/'+questNumber+'/'+ score +'/'+lesson+'/'+page+'/';
		showModal(modal);
	}
}

function questFinishSimple(modal,questNumber,lesson,page,target) {
	var hits = document.getElementById("hits");

	if (Number(hits.innerHTML) < target){
		alert('Você ainda não acertou todas as respostas');
	} else {
		var totalScore = document.getElementById("totalScore");
		score = totalScore.innerHTML;
		var questCaption = document.getElementById("questCaption");
		var reward = document.getElementById("reward");
		if (score == target){
			questCaption.innerHTML = 'Você fez a pontuação máxima.';
		} else if (score >= 0){
			questCaption.innerHTML = 'Você poderia ter marcado mais pontos, mas podera tentar novamente se quiser.';
		} else {
			questCaption.innerHTML = 'Você marcou uma pontuação negativa, Você receberá 0 pontos';
			score = 0;
		}
		reward.innerHTML = 'Você ganhou: '+ score +' pontos, '+ score +' créditos e um troféu joinha';
		document.getElementById("conclud").href = '/questConclude/'+questNumber+'/'+ score +'/'+lesson+'/'+page+'/';
		showModal(modal);
	}
}
function hitWord(){
	riseScore();
}

function c(charID){ //caça palavras
	wordID = charID.charAt(0);
	var char = document.getElementById(charID);
	var word = document.getElementById(wordID);
	word.value = word.value - 1;
	char.style ="background-color: #00008B; color: white;";
	char.onclick = "";
	if (word.value <= 0){
		hitWord();	
		word.style.backgroundColor = "green";
	}
}

function cw(letter,target){ //palavras cruzadas
	var word = document.getElementById(target.charAt(0));
	var wLetter = target.charAt(1);
	if (letter.value.toUpperCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '') == wLetter){
		word.value -= 1;
		letter.readOnly = true; 
		if (word.value <= 0){
			hitWord();
			word.classList.add("green");
		}
	} else {
	    letter.placeholder = letter.value;
	    letter.value = '';
	}
	if (letter.value.length == 1 || letter.placeholder.length == 1){
		var nextIndex = letter.tabIndex + 1;
		if(letter.tabIndex == 125) {
		    nextIndex = 0;
		}
		var tabbables = document.querySelectorAll("input");
		for(var i=0; i<tabbables.length; i++) {
		    if(tabbables[i].tabIndex == nextIndex) { 
		        tabbables[i].focus(); 
		        break;
		    }
		}
    }
}

function answareText(modal,quest){
	var score = 0;
	var text = '';
	var reward = document.getElementById("reward");
	if (quest == '3-1'){
		var answare1 = {"nome": document.getElementById("nome1").value, "prato": document.getElementById("prato1").value, "cor": document.getElementById("cor1").value, "esporte": document.getElementById("esporte1").value, "programa": document.getElementById("programa1").value, "lazer": document.getElementById("lazer1").value};
		var answare2 = {"nome": document.getElementById("nome2").value, "prato": document.getElementById("prato2").value, "cor": document.getElementById("cor2").value, "esporte": document.getElementById("esporte2").value, "programa": document.getElementById("programa2").value, "lazer": document.getElementById("lazer2").value};
		var answare3 = {"nome": document.getElementById("nome3").value, "prato": document.getElementById("prato3").value, "cor": document.getElementById("cor3").value, "esporte": document.getElementById("esporte3").value, "programa": document.getElementById("programa3").value, "lazer": document.getElementById("lazer3").value};
		text = answare1["nome"] + "_" + answare1["prato"] + "_" + answare1["cor"] + "_" + answare1["esporte"] + "_" + answare1["programa"] + "_" + answare1["lazer"] + "#" +
			answare2["nome"] + "_" + answare2["prato"] + "_" + answare2["cor"] + "_" + answare2["esporte"] + "_" + answare2["programa"] + "_" + answare2["lazer"] + "#" +
			answare3["nome"] + "_" + answare3["prato"] + "_" + answare3["cor"] + "_" + answare3["esporte"] + "_" + answare3["programa"] + "_" + answare3["lazer"];
		finish = text.replace(/\s/g,'');
		var empty = finish.search("____");
		if (empty != -1){
			score = 5;
			reward.innerHTML = 'Você ganhou apenas 5 pontos e 5 créditos, pois deixou muitos espaços em branco.';
		} else {
			var empty = finish.search("__");
			if (empty != -1){
				score = 25;
				reward.innerHTML = 'Você ganhou apenas 25 pontos e 25 créditos, pois deixou algum espaço em branco.';
			} else {
				score = 50;
				reward.innerHTML = 'Parabéns! Você ganhou 50 pontos e 50 créditos!';
			}
		}
	} else if (quest == '4-1' || quest == '9-1' || quest == '9-4' || quest == '9-5' || quest == '17-1'){
		text = document.getElementById("ftext").value;
		score = document.getElementById("totalScore").innerHTML;
	} else if (quest == '15-2'){
		var ok = true;
		var answare1 = document.getElementById("quest1").getElementsByTagName("INPUT")[0].value;
		if (answare1 == 'Sim'){
			var answare2 = document.getElementById("quest2").getElementsByTagName("INPUT");
			if(answare2.length > 1){ok = false;} else {answare2 = document.getElementById("quest2").getElementsByTagName("INPUT")[0].value;}
			var answare3 = document.getElementById("quest3").getElementsByTagName("INPUT");
			if(answare3.length > 1){ok = false;} else {answare3 = document.getElementById("quest3").getElementsByTagName("INPUT")[0].value;}
			var answare4 = document.getElementById("quest4").getElementsByTagName("INPUT");
			if(answare4.length > 1){ok = false;} else {answare4 = document.getElementById("quest4").getElementsByTagName("INPUT")[0].value;}
			var answare5 = document.getElementById("quest5").getElementsByTagName("INPUT");
			if(answare5.length > 1){ok = false;} else {answare5 = document.getElementById("quest5").getElementsByTagName("INPUT")[0].value;}
			text ="Você se recorda de alguma apresentação de que você participou? - " + answare1 + "__" +
				"Que tipo de apresentação era? - " + answare2 + "__" +
				"Como foi essa experiência? - " + answare3 + "__" +
				"Ao final da apresentação, você foi aplaudido? - " + answare4 + "__" +
				"Como se sentiu? - " + answare5;
		} else{
			text = "Você se recorda de alguma apresentação de que você participou? - " + answare1;
		}
		if (ok){
			score = document.getElementById("totalScore").innerHTML;
			reward.innerHTML = 'Parabéns! Você ganhou '+ score +' pontos e '+ score +' créditos!';
		} else {
			score = 0;
		}
	} else if (quest == '18-1'){
		if (document.getElementById("hits").innerHTML < 6){
			score == 0;
		} else {
			score = document.getElementById("totalScore").innerHTML;
			text = document.getElementById("aPo").value + "_" + document.getElementById("aPa").value + "#" + document.getElementById("aMo").value + "_" +
				document.getElementById("aMa").value + " & " + document.getElementById("pai").value + "_" + document.getElementById("mae").value;
			reward.innerHTML = 'Parabéns! Você ganhou '+ score +' pontos e '+ score +' créditos!';
		}
		
	}
	if (score == '0'){
		alert('Parece que você ainda não respondeu tudo');
	} else {
		text = text.replace(/\s/g,'+');
		document.getElementById("text").value = quest+' '+text + ' ' + score;
		showModal(modal);
	}
}

function textSize(text,target){
	var answare = document.getElementById("ftext");
	var score = document.getElementById("totalScore");
	var half = Math.round(target/2);
	var min = Math.round(target/10);
	if (answare.value.length > target){
		score.innerHTML = target;
		reward.innerHTML = 'Parabéns! Você ganhou '+target+' pontos e '+target+' créditos!';
	} else if (answare.value.length > half){
		score.innerHTML = half;
		reward.innerHTML = 'Você ganhou '+half+' pontos e '+half+' créditos! Você está na média.';		
	} else {
		score.innerHTML = min;
		reward.innerHTML = 'Você ganhou apenas '+min+' pontos e '+min+' créditos porque escreveu muito pouco.';
	}
}

function textFinish(btn, text, allow){
	document.getElementById(text).readOnly = true;
	btn.remove(); 
	for(var i=0; i<allow.length; i++) {
		document.getElementById(allow[i]).disabled = false;
	}
}

function values(answare,values){
	var value = 0;
	var reward = document.getElementById(answare);
	var score = hit = 0;
	for (i = 0; i < values.length; i++) {
		var item = document.getElementById(values[i]);
		if (item.value != ''){
			score += 10; 
			hit += 1;
		}
		value += Number(item.value);
	}
	document.getElementById("totalScore").innerHTML = score;
	document.getElementById("hits").innerHTML = hit;
	reward.value = value.toFixed(2);	
}

function selectAnsware(selected,toDelete){
	riseScore();
	selected.onclick = '';
	for(var i=0; i<toDelete.length; i++) {
		document.getElementById(toDelete[i]).remove();
	}
}
function selectWrong(selected){
	document.getElementById("totalScore").innerHTML = Number(document.getElementById("totalScore").innerHTML) - 5;
	selected.parentElement.style.backgroundColor = "#FFA384";
}

function selectPoint(point){
	riseScore();
	point.style.fillOpacity = '24%';
	point.style.strokeOpacity = '100%';
	point.onclick = "";
}
function selectDrawPoint(point){
	document.getElementById("totalScore").innerHTML = Number(document.getElementById("totalScore").innerHTML) + 1;
	document.getElementById("hits").innerHTML = Number(document.getElementById("hits").innerHTML) + 1;
	point.style.fillOpacity = '25%';
	point.style.strokeOpacity = '30%';
	point.onclick = "";
}

function drawLine(point, line, group){
	pGroup = document.getElementById(group);
	if (pGroup.value == line[0]){
		selectDrawPoint(point);
		document.getElementById(line[0]).style.strokeOpacity = '100%';
		pGroup.value = line[1];
	}
}

function riseScore(){
	document.getElementById("totalScore").innerHTML = Number(document.getElementById("totalScore").innerHTML) + 10;
	document.getElementById("hits").innerHTML = Number(document.getElementById("hits").innerHTML) + 1;
}

function selectItem(item){
	var selected = document.getElementById("selected");
	var old = document.getElementById(selected.value);
	if (old != undefined){
		old.style.backgroundColor = "#E0FFFF";
	}
	selected.value = item.id;
	item.style.backgroundColor = "#51BAC8";
}
function useItem(use,item){
	var selected = document.getElementById("selected");
	var sItem = document.getElementById(selected.value);
	if (sItem != undefined){
		if (selected.value == item){
			riseScore();
			sItem.remove();
			use.remove();
			if (document.getElementById("options").childElementCount <= 0){
				finished();
			}
		} else {
			sItem.style.backgroundColor = "#FFB3B3";
			document.getElementById("totalScore").innerHTML = Number(document.getElementById("totalScore").innerHTML) - 1;
		}
	}
}

function delItem(item){
	if (item.id == 'notDel'){
		item.style="background-color: #FFA384;";
		document.getElementById("totalScore").innerHTML = Number(document.getElementById("totalScore").innerHTML) - 5;
	} else {
		item.remove();
		riseScore();
	}
}

function finished(){
	document.getElementById("imgGame").style.opacity = "1";
	document.getElementById("finishBtn").className = "button";
}

function showItem(item){
	i = document.getElementById(item).parentElement;
	if (i.className == "box sunny large"){
		i.className = "hide";
	} else {
		i.className = "box sunny large";
	}
}

function reply(answer){
	stage = document.getElementById(answer.name)
    stageNumber = Number(answer.name.slice(-1));
    if (stageNumber == 5){
    	document.getElementById("btnTerminar").style.display = "Block"
    } else {
		stageNext = document.getElementById(answer.name.replace(stageNumber, stageNumber + 1));
		stageNext.src = stage.src;
    }
    if (answer.value == 'True'){
		stage.src = document.getElementById("good").value;
		riseScore();
	}
	else{
		stage.src = document.getElementById("bad").value;
		stage.style.width = "40%";
		document.getElementById("hits").innerHTML = Number(document.getElementById("hits").innerHTML) + 1;
	}
	question = answer.parentElement.parentElement;
	question.style.display = "none"
	qNumber = Number(question.id.slice(-1));
	if (qNumber < 5){
		qNext = document.getElementById(question.id.replace(qNumber, qNumber + 1));
		qNext.style.display = "block";
	}
}


function saveCity(item,choice){
	gCity = document.getElementById("gCity");
	bCity = document.getElementById("bCity");
	cSize = document.getElementById("cSize");
	ready = document.getElementById("ready");
	if (choice == "Good"){
		cSize.value = Number(cSize.value) + 10;
		cSize.name = Number(cSize.name) - 10;
		ready.value = Number(ready.value) + 1;
	} else {
		cSize.value = Number(cSize.value) - 10;
		cSize.name = Number(cSize.name) + 10;
	}
	gCity.style.width = cSize.value+"%";
	bCity.style.width = cSize.name+"%";
	item.remove();
	if (ready.value >= 5){
		btn = document.getElementById("btnFinish")
		btn.style.display = "block";
		btn.scrollIntoView();
	} else {
	    gCity.scrollIntoView();
	}
}

function clearCity(modal,questNumber,lesson,page) {
	score = document.getElementById("cSize").value;
	var questCaption = document.getElementById("questCaption");
	var reward = document.getElementById("reward");

	if (score == 100){
		questCaption.innerHTML = 'Você salvou a cidade!';
	} else if (score >= 50){
		questCaption.innerHTML = 'Você ajudou a cidade, mas poderia fazer melhor.';
	} else {
		questCaption.innerHTML = 'Sua cidade está arruinada';
		score = 0;
	}
	reward.innerHTML = 'Você ganhou: '+ score +' pontos, '+ score +' créditos e um troféu joinha';
	document.getElementById("conclud").href = '/questConclude/'+questNumber+'/'+ score +'/'+lesson+'/'+page+'/';
	showModal(modal);
}

function familyFree(member){
	if (member.name != 'ok'){
		if (member.value.length >= 3){
			riseScore();
			member.name = 'ok';
		}
	} else {
		if (member.value.length <= 1){
			document.getElementById("totalScore").innerHTML = Number(document.getElementById("totalScore").innerHTML) - 10;
			document.getElementById("hits").innerHTML = Number(document.getElementById("hits").innerHTML) - 1;
			member.name = 'not';
		}
	}
}

function scrollMenu() {
	bar = document.getElementById("leftBtn");
	if (document.body.scrollTop > 300 || document.documentElement.scrollTop > 300) {
		bar.style.position = 'fixed';
		bar.style.transform = 'scale(0.5,0.5)';
		bar.style.top = '0px';
		bar.innerHTML = bar.innerHTML.replace('Lição','<input type="hidden">');
	} else {
		bar.style.position= 'static';
		bar.style.transform = 'scale(1,1)';
		bar.innerHTML = bar.innerHTML.replace('<input type="hidden">','Lição');
	}
}
