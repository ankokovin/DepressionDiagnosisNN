function start(){
    console.log("Started")
    window.location.href = '/test';
}

function load_model_list(){
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/models', false);
    xhr.send();
    if (xhr.status != 200) {
    alert( xhr.status + ': ' + xhr.statusText ); // пример вывода: 404: Not Found
    } else {
        models = JSON.parse(xhr.responseText); 
        html="";
        for(const model of models) {
            let name = null;
            if (model.name){name=model.name+" "+model.uuid;}else{name=model.uuid}
           html += "<div class=\"list-group-item list-group-item-action\"";
           html+= "><button class=\"btn ";
           if(model.main) html +="btn-primary"; else html +="btn-secondary"
           html += "\"type=\"button\" onClick=\"set_new_main('"+ model.uuid +"')\">"+name+"</button>";
           html += "<button class=\"btn btn-danger\" onClick=\"delete_model('"+model.uuid+"')\">Удалить</button>";
           html += "</div>"
        }
        document.getElementById('model-list').innerHTML = html;
    }
}

function delete_model(model_uuid){
    var xhr = new XMLHttpRequest();
    xhr.open('DELETE', '/delete_model/'+model_uuid, false);
    xhr.send();
    load_model_list();
}

function set_new_main(uuid){
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/set_main/'+uuid, false);
    xhr.send();
    if (xhr.status != 200) {
        alert( xhr.status + ': ' + xhr.statusText ); // пример вывода: 404: Not Found
        } else {
            load_model_list()
        }
}

function send_to_diagnose(){
    elements = document.getElementsByClassName('field-input');
    query = {'items':[]}
    for (const element of elements) {
        let name = element.id;
        let tag = element.tagName.toLowerCase();
        let val = element.value;
        if (val == ''){
            //TODO: show error?
            return;
        }
        query['items'].push({
            'value':val,
            'name':name
        })
            
    }
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/diagnose/', false);
    query = JSON.stringify(query)
    console.log(query)
    xhr.send(query);
    if (xhr.status!=200){
        alert( xhr.status + ': ' + xhr.statusText ); // пример вывода: 404: Not Found
    } else {
        window.location.href = '/result/'+xhr.responseText
    }
}