process.stdin.resume();
process.stdin.setEncoding('utf8');

// your code goes here

ent = {
    "_version": "3.0",
    "identification": {
      "id": "/UI2/SAP_KPIFRW5_TCR_S",
      "title": "{{title}}",
      "entityType": "role"
    },
    "payload": {
      "catalogs": [
        {
          "id": "/UI2/SAP_KPIFRW5_TC_S"
        }
      ],
      "groups": [1,2,3],
      "apps": [
        {
          "id": "106FFF9E51281C56BB7A6A4F48F735FF"
        }
      ]
    },
    "texts": [
      {
        "locale": "",
        "textDictionary": {
          "title": "SAP Role for KPI Framework"
        }
      },
      {
        "locale": "zh-CN",
        "textDictionary": {
          "title": "KPI 框架的 SAP 角色"
        }
      },
      {
        "locale": "th",
        "textDictionary": {
          "title": "บทบาท SAP สำหรับ KPI Framework"
        }
      },
      {
        "locale": "ko",
        "textDictionary": {
          "title": "KPI 프레임워크의 SAP 역할"
        }
      },
      {
        "locale": "ro",
        "textDictionary": {
          "title": "Rol SAP pt.framework KPI"
        }
      },
      {
        "locale": "sl",
        "textDictionary": {
          "title": "SAP-vloga za KPI-Framework"
        }
      },
      {
        "locale": "hr",
        "textDictionary": {
          "title": "SAP uloga za okvir KPIja"
        }
      },
      {
        "locale": "uk",
        "textDictionary": {
          "title": "Роль SAP для архітектури KPI"
        }
      },
      {
        "locale": "et",
        "textDictionary": {
          "title": "KPI raamistiku SAP-i roll"
        }
      },
      {
        "locale": "ar",
        "textDictionary": {
          "title": "SAP: دور إطار عمل مؤشرات الأداء الأساسية"
        }
      },
      {
        "locale": "he",
        "textDictionary": {
          "title": "תפקיד SAP עבור מסגרת KPI"
        }
      },
      {
        "locale": "cs",
        "textDictionary": {
          "title": "Role SAP pro framework KPI"
        }
      },
      {
        "locale": "de",
        "textDictionary": {
          "title": "SAP-Rolle für KPI-Framework"
        }
      },
      {
        "locale": "en",
        "textDictionary": {
          "title": "SAP Role for KPI Framework"
        }
      },
      {
        "locale": "fr",
        "textDictionary": {
          "title": "Rôle SAP pour framework du KPI"
        }
      },
      {
        "locale": "el",
        "textDictionary": {
          "title": "Ρόλος SAP για KPI Framework"
        }
      },
      {
        "locale": "hu",
        "textDictionary": {
          "title": "KPI-framework SAP-szerepe"
        }
      },
      {
        "locale": "it",
        "textDictionary": {
          "title": "Ruolo SAP per Framework KPI"
        }
      },
      {
        "locale": "ja",
        "textDictionary": {
          "title": "KPI フレームワークの SAP ロール"
        }
      },
      {
        "locale": "da",
        "textDictionary": {
          "title": "SAP-rolle for KPI-framework"
        }
      },
      {
        "locale": "pl",
        "textDictionary": {
          "title": "Rola SAP dla framework KPI"
        }
      },
      {
        "locale": "zh-TW",
        "textDictionary": {
          "title": "關鍵效能指標架構的 SAP 角色"
        }
      },
      {
        "locale": "nl",
        "textDictionary": {
          "title": "SAP-rol voor KPI-framework"
        }
      },
      {
        "locale": "no",
        "textDictionary": {
          "title": "SAP-rolle for KPI-framework"
        }
      },
      {
        "locale": "pt",
        "textDictionary": {
          "title": "Função SAP para framework KPI"
        }
      },
      {
        "locale": "sk",
        "textDictionary": {
          "title": "Rola SAP pre framework KPI"
        }
      },
      {
        "locale": "ru",
        "textDictionary": {
          "title": "Роль SAP для архитектуры KPI"
        }
      },
      {
        "locale": "es",
        "textDictionary": {
          "title": "Rol SAP para framework KPI"
        }
      },
      {
        "locale": "tr",
        "textDictionary": {
          "title": "KPI çerçevesi için SAP rolü"
        }
      },
      {
        "locale": "fi",
        "textDictionary": {
          "title": "SAP-rooli KPI-kehystä varten"
        }
      },
      {
        "locale": "sv",
        "textDictionary": {
          "title": "SAP-roll för KPI-framework"
        }
      },
      {
        "locale": "bg",
        "textDictionary": {
          "title": "SAP роля за KPI структура"
        }
      },
      {
        "locale": "lt",
        "textDictionary": {
          "title": "SAP vaidmuo, skirtas KPI sistemai"
        }
      },
      {
        "locale": "lv",
        "textDictionary": {
          "title": "KPI ietvarprogrammas SAP loma"
        }
      },
      {
        "locale": "ca",
        "textDictionary": {
          "title": "Rol de SAP per a estructura de KPI"
        }
      },
      {
        "locale": "sr-Latn",
        "textDictionary": {
          "title": "SAP uloga za okvir pokazatelja ključnog izvođenja"
        }
      },
      {
        "locale": "hi",
        "textDictionary": {
          "title": "KPI फ्रेमवर्क के लिए SAP भूमिका"
        }
      },
      {
        "locale": "kk",
        "textDictionary": {
          "title": "KPI архитектурасына арналған SAP рөлі"
        }
      },
      {
        "locale": "vi",
        "textDictionary": {
          "title": "Vai trò SAP cho cơ cấu KPI"
        }
      }
    ]
  };
  
  total = 0;
  max = 4;
  ids=[]
  console.log(typeof(ent.payload));
  if (ent.payload && ( typeof(ent.payload) === 'object' )) {
  	// for (const [k,v] of Object.entries(ent.payload)) {
  	for (const v of Object.values(ent.payload)) {
  		if (Array.isArray(v)) {
  			total+=v.length;
  			if (total > max) {
                console.log(`max ${max} exceeded`);
                ids.push(ent.identification.id)
  				break;
  			}
  		}
  		}
  
  	}
  	console.log('total payload sub arrays length:', total);
  	console.log('entity IDs:', ids);
  
  

