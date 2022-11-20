
'use strict';

// const fs = require('fs');
define(['require', 'fs'], fs(require)); {
    var fs = require('fs');
};


function googleTranslateElementInit() {
    new google.translate.TranslateElement({pageLanguage: 'sp'}, 'google_translate_element');
}

function getOption() {
    selectElement = document.querySelector('#LanguageSelect');
    output = selectElement.value;
    console.log(output)
    document.querySelector('.output').textContent = output;
}

console.log('Hello');

const customer = {
    name: "Newbie Co.",
    order_count: 0,
    address: "Po Box City",
};

let  jsonString = JSON.stringify(customer);
fs.writeFile('./newCustomer.json', jsonString, (err) => {
    if (err) throw err;

    console.log('Successfully wrote file');
    
});



