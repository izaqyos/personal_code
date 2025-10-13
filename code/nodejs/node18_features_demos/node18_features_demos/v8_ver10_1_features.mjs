import { setTimeout } from 'timers/promises';

console.log('Demo new features in V8 10.1');


console.log('Locale improvements. mainly added properties: calendars, collations, hourCycles, numberingSystems, timeZones, textInfo, and weekInfo.');
function printIntlLocaleDetails(localeStr) {
    console.log('Printing locale', localeStr);
    try {
        const locale= new Intl.Locale(localeStr);
        console.log(`${locale} details:`);
        console.log(`locale calendar: ${locale.calendars}, collations: ${locale.collations}, hourCycles: ${locale.hourCycles}, numberingSystems: ${locale.numberingSystems}, writing direction: ${JSON.stringify(locale.textInfo)}, week info: ${JSON.stringify(locale.weekInfo)}`);
        console.log('locale timeZones', locale.timeZones);
    }
    catch (err) {
        console.log(`cant init locale due to error ${err.name} ${err.message}`);
    }
}
//const eUSLocale= new Intl.Locale('en-us');
// printIntlLocaleDetails('en-us');

function allLocalesDetails() {
//Locale list courtesy of SAP help :) - https://help.sap.com/docs/SAP_BUSINESSOBJECTS_BUSINESS_INTELLIGENCE_PLATFORM/09382741061c40a989fae01e61d54202/46758c5e6e041014910aba7db0e91070.html?locale=en-US
const all_locales=[	'af-ZA',	'sq-AL',	'ar-DZ',	'ar-BH',	'ar-EG',	'ar-IQ',	'ar-JO',	'ar-KW',	'ar-LB',	'ar-LY',	'ar-MA',	'ar-OM',	'ar-QA',	'ar-SA',	'ar-SY',	'ar-TN',	'ar-AE',	'ar-YE',	'hy-AM',	'az-AZ',	'eu-ES',	'be-BY',	'bn-IN',	'bs-BA',	'bg-BG',	'ca-ES',	'zh-CN',	'zh-HK',	'zh-MO',	'zh-SG',	'zh-TW',	'hr-HR',	'cs-CZ',	'da-DK',	'nl-BE',	'nl-NL',	'en-AU',	'en-BZ',	'en-CA',	'en-IE',	'en-JM',	'en-NZ',	'en-PH',	'en-ZA',	'en-TT',	'en-VI',	'en-GB',	'en-US',	'en-ZW',	'et-EE',	'fo-FO',	'fi-FI',	'fr-BE',	'fr-CA',	'fr-FR',	'fr-LU',	'fr-MC',	'fr-CH',	'gl-ES',	'ka-GE',	'de-AT',	'de-DE',	'de-LI',	'de-LU',	'de-CH',	'el-GR',	'gu-IN',	'he-IL',	'hi-IN',	'hu-HU',	'is-IS',	'id-ID',	'it-IT',	'it-CH',	'ja-JP',	'kn-IN',	'kk-KZ',	'kok-IN',	'ko-KR',	'lv-LV',	'lt-LT',	'mk-MK',	'ms-BN',	'ms-MY',	'ml-IN',	'mt-MT',	'mr-IN',	'mn-MN',	'se-NO',	'nb-NO',	'nn-NO',	'fa-IR',	'pl-PL',	'pt-BR',	'pt-PT',	'pa-IN',	'ro-RO',	'ru-RU',	'sr-BA',	'sr-CS',	'sk-SK',	'sl-SI',	'es-AR',	'es-BO',	'es-CL',	'es-CO',	'es-CR',	'es-DO',	'es-EC',	'es-SV',	'es-GT',	'es-HN',	'es-MX',	'es-NI',	'es-PA',	'es-PY',	'es-PE',	'es-PR',	'es-ES',	'es-UY',	'es-VE',	'sw-KE',	'sv-FI',	'sv-SE',	'syr-SY',	'ta-IN',	'te-IN',	'th-TH',	'tn-ZA',	'tr-TR',	'uk-UA',	'uz-UZ',	'vi-VN',	'cy-GB',	'xh-ZA',	'zu-ZA',];	
}

const all_locale_abber = [['Afrikaans (South Africa)',	'af-ZA'], ['Albanian (Albania)',	'sq-AL'], ['Arabic (Algeria)',	'ar-DZ'], ['Arabic (Bahrain)',	'ar-BH'], ['Arabic (Egypt)',	'ar-EG'], ['Arabic (Iraq)',	'ar-IQ'], ['Arabic (Jordan)',	'ar-JO'], ['Arabic (Kuwait)',	'ar-KW'], ['Arabic (Lebanon)',	'ar-LB'], ['Arabic (Libya)',	'ar-LY'], ['Arabic (Morocco)',	'ar-MA'], ['Arabic (Oman)',	'ar-OM'], ['Arabic (Qatar)',	'ar-QA'], ['Arabic (Saudi Arabia)',	'ar-SA'], ['Arabic (Syria)',	'ar-SY'], ['Arabic (Tunisia)',	'ar-TN'], ['Arabic (United Arab Emirates)',	'ar-AE'], ['Arabic (Yemen)',	'ar-YE'], ['Armenian (Armenia)',	'hy-AM'], ['Azerbaijani (Azerbaijan)',	'az-AZ'], ['Basque (Spain)',	'eu-ES'], ['Belarusian (Belarus)',	'be-BY'], ['Bengali (India)',	'bn-IN'], ['Bosnian (Bosnia and Herzegovina)',	'bs-BA'], ['Bulgarian (Bulgaria)',	'bg-BG'], ['Catalan (Spain)',	'ca-ES'], ['Chinese (China)',	'zh-CN'], ['Chinese (Hong Kong SAR China)',	'zh-HK'], ['Chinese (Macao SAR China)',	'zh-MO'], ['Chinese (Singapore)',	'zh-SG'], ['Chinese (Taiwan)',	'zh-TW'], ['Croatian (Croatia)',	'hr-HR'], ['Czech (Czech Republic)',	'cs-CZ'], ['Danish (Denmark)',	'da-DK'], ['Dutch (Belgium)',	'nl-BE'], ['Dutch (Netherlands)',	'nl-NL'], ['English (Australia)',	'en-AU'], ['English (Belize)',	'en-BZ'], ['English (Canada)',	'en-CA'], ['English (Ireland)',	'en-IE'], ['English (Jamaica)',	'en-JM'], ['English (New Zealand)',	'en-NZ'], ['English (Philippines)',	'en-PH'], ['English (South Africa)',	'en-ZA'], ['English (Trinidad and Tobago)',	'en-TT'], ['English (U.S. Virgin Islands)',	'en-VI'], ['English (United Kingdom)',	'en-GB'], ['English (United States)',	'en-US'], ['English (Zimbabwe)',	'en-ZW'], ['Estonian (Estonia)',	'et-EE'], ['Faroese (Faroe Islands)',	'fo-FO'], ['Finnish (Finland)',	'fi-FI'], ['French (Belgium)',	'fr-BE'], ['French (Canada)',	'fr-CA'], ['French (France)',	'fr-FR'], ['French (Luxembourg)',	'fr-LU'], ['French (Monaco)',	'fr-MC'], ['French (Switzerland)',	'fr-CH'], ['Galician (Spain)',	'gl-ES'], ['Georgian (Georgia)',	'ka-GE'], ['German (Austria)',	'de-AT'], ['German (Germany)',	'de-DE'], ['German (Liechtenstein)',	'de-LI'], ['German (Luxembourg)',	'de-LU'], ['German (Switzerland)',	'de-CH'], ['Greek (Greece)',	'el-GR'], ['Gujarati (India)',	'gu-IN'], ['Hebrew (Israel)',	'he-IL'], ['Hindi (India)',	'hi-IN'], ['Hungarian (Hungary)',	'hu-HU'], ['Icelandic (Iceland)',	'is-IS'], ['Indonesian (Indonesia)',	'id-ID'], ['Italian (Italy)',	'it-IT'], ['Italian (Switzerland)',	'it-CH'], ['Japanese (Japan)',	'ja-JP'], ['Kannada (India)',	'kn-IN'], ['Kazakh (Kazakhstan)',	'kk-KZ'], ['Konkani (India)	k','ok-IN'], ['Korean (South Korea)',	'ko-KR'], ['Latvian (Latvia)',	'lv-LV'], ['Lithuanian (Lithuania)',	'lt-LT'], ['Macedonian (Macedonia)',	'mk-MK'], ['Malay (Brunei)',	'ms-BN'], ['Malay (Malaysia)',	'ms-MY'], ['Malayalam (India)',	'ml-IN'], ['Maltese (Malta)',	'mt-MT'], ['Marathi (India)',	'mr-IN'], ['Mongolian (Mongolia)',	'mn-MN'], ['Northern Sami (Norway)',	'se-NO'], ['Norwegian Bokml (Norway)',	'nb-NO'], ['Norwegian Nynorsk (Norway)',	'nn-NO'], ['Persian (Iran)',	'fa-IR'], ['Polish (Poland)',	'pl-PL'], ['Portuguese (Brazil)',	'pt-BR'], ['Portuguese (Portugal)',	'pt-PT'], ['Punjabi (India)',	'pa-IN'], ['Romanian (Romania)',	'ro-RO'], ['Russian (Russia)',	'ru-RU'], ['Serbian (Bosnia and Herzegovina)',	'sr-BA'], ['Serbian (Serbia And Montenegro)',	'sr-CS'], ['Slovak (Slovakia)',	'sk-SK'], ['Slovenian (Slovenia)',	'sl-SI'], ['Spanish (Argentina)',	'es-AR'], ['Spanish (Bolivia)',	'es-BO'], ['Spanish (Chile)',	'es-CL'], ['Spanish (Colombia)',	'es-CO'], ['Spanish (Costa Rica)',	'es-CR'], ['Spanish (Dominican Republic)',	'es-DO'], ['Spanish (Ecuador)',	'es-EC'], ['Spanish (El Salvador)',	'es-SV'], ['Spanish (Guatemala)',	'es-GT'], ['Spanish (Honduras)',	'es-HN'], ['Spanish (Mexico)',	'es-MX'], ['Spanish (Nicaragua)',	'es-NI'], ['Spanish (Panama)',	'es-PA'], ['Spanish (Paraguay)',	'es-PY'], ['Spanish (Peru)',	'es-PE'], ['Spanish (Puerto Rico)',	'es-PR'], ['Spanish (Spain)',	'es-ES'], ['Spanish (Uruguay)',	'es-UY'], ['Spanish (Venezuela)',	'es-VE'], ['Swahili (Kenya)',,	'sw-KE'], ['Swedish (Finland)',	'sv-FI'], ['Swedish (Sweden)',	'sv-SE'], ['Syriac (Syria)	s','yr-SY'], ['Tamil (India)',	'ta-IN'], ['Telugu (India)',	'te-IN'], ['Thai (Thailand)',	'th-TH'], ['swana (South Africa)',	'tn-ZA'], ['Turkish (Turkey)',	'tr-TR'], ['Ukrainian (Ukraine)',	'uk-UA'], ['Uzbek (Uzbekistan)',	'uz-UZ'], ['Vietnamese (Vietnam)',	'vi-VN'], ['Welsh (United Kingdom)',	'cy-GB'], ['Xhosa (South Africa)',	'xh-ZA'], ['Zulu (South Africa)',	'zu-ZA'],];

let pauseTimes=0;
console.log('--------------------------------------------------------------------------------');
for (const locale_abber of all_locale_abber) {
    pauseTimes++;
    if (pauseTimes == 5){
        console.log('--------------------------------------------------------------------------------');
        await setTimeout(1500);
        pauseTimes = 0;
    }
    console.log(`Printing the details of locale ${locale_abber[0]} ${locale_abber[1]}`);
    printIntlLocaleDetails(locale_abber[1]);
}

console.log('--------------------------------------------------------------------------------');
console.log('Locale improvements. get array of supported values in V8 for Intl APIs using Intl.supportedValuesOf(code). code can be calander, collation, currency, numberingSystems, timeZone etc');
console.log(Intl.supportedValuesOf('calendar'));
await setTimeout(1000);
console.log('--------------------------------------------------------------------------------');
console.log(Intl.supportedValuesOf('collation'));
await setTimeout(1000);
console.log('--------------------------------------------------------------------------------');
console.log(Intl.supportedValuesOf('currency'));
await setTimeout(1000);
console.log('--------------------------------------------------------------------------------');
console.log(Intl.supportedValuesOf('numberingSystem'));
await setTimeout(1000);
console.log('--------------------------------------------------------------------------------');
console.log(Intl.supportedValuesOf('timeZone'));
await setTimeout(1000);
console.log('--------------------------------------------------------------------------------');

console.log('Array findLast and findLastIndex...');
const myArray = [
    {val: 1 },
    {val: 2 },
    {val: 3 },
    {val: 4 },
    {val: 5 },
    {val: 6 },
    {val: 7 },
    {val: 8 },
    {val: 9 },
    {val: 10},
    {val: 11},
];

console.log(`Find element divisible by 5 ${JSON.stringify(myArray.find( elem => elem.val %5 == 0))}`);
console.log(`Find last element divisible by 5 ${JSON.stringify(myArray.findLast( elem => elem.val %5 == 0))}`);
console.log(`Find index of element divisible by 5 ${myArray.findIndex( elem => elem.val %5 == 0)}`);
console.log(`Find index of last element divisible by 5 ${myArray.findLastIndex( elem => elem.val %5 == 0)}`);
console.log('--------------------------------------------------------------------------------');

