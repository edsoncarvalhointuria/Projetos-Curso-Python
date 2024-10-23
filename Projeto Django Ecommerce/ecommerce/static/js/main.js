var url = new URL(document.URL);
var itens = document.getElementsByClassName("item-order");

for (i = 0; i < itens.length; i++){
    url.searchParams.set("order", itens[i].value);
    itens[i].value = url.href;
}