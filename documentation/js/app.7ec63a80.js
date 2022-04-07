(function(e){function t(t){for(var i,s,a=t[0],c=t[1],l=t[2],p=0,u=[];p<a.length;p++)s=a[p],Object.prototype.hasOwnProperty.call(r,s)&&r[s]&&u.push(r[s][0]),r[s]=0;for(i in c)Object.prototype.hasOwnProperty.call(c,i)&&(e[i]=c[i]);d&&d(t);while(u.length)u.shift()();return o.push.apply(o,l||[]),n()}function n(){for(var e,t=0;t<o.length;t++){for(var n=o[t],i=!0,a=1;a<n.length;a++){var c=n[a];0!==r[c]&&(i=!1)}i&&(o.splice(t--,1),e=s(s.s=n[0]))}return e}var i={},r={app:0},o=[];function s(t){if(i[t])return i[t].exports;var n=i[t]={i:t,l:!1,exports:{}};return e[t].call(n.exports,n,n.exports,s),n.l=!0,n.exports}s.m=e,s.c=i,s.d=function(e,t,n){s.o(e,t)||Object.defineProperty(e,t,{enumerable:!0,get:n})},s.r=function(e){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},s.t=function(e,t){if(1&t&&(e=s(e)),8&t)return e;if(4&t&&"object"===typeof e&&e&&e.__esModule)return e;var n=Object.create(null);if(s.r(n),Object.defineProperty(n,"default",{enumerable:!0,value:e}),2&t&&"string"!=typeof e)for(var i in e)s.d(n,i,function(t){return e[t]}.bind(null,i));return n},s.n=function(e){var t=e&&e.__esModule?function(){return e["default"]}:function(){return e};return s.d(t,"a",t),t},s.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)},s.p="/";var a=window["webpackJsonp"]=window["webpackJsonp"]||[],c=a.push.bind(a);a.push=t,a=a.slice();for(var l=0;l<a.length;l++)t(a[l]);var d=c;o.push([0,"chunk-vendors"]),n()})
(
{0:function(e,t,n){e.exports=n("56d7")},"12c0":function(e,t,n){},"56d7":function(e,t,n){"use strict";n.r(t);n("e260"),n("e6cf"),n("cca6"),n("a79d");var i=n("2b0e"),r=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("main",[n("div",{attrs:{id:"wrapper"}},[e._m(0),n("nav",e._l(e.elementsList,(function(t){return n("div",{key:t.id,staticClass:"elementInList"},[n("div",{on:{click:function(n){return e.setValuesForDocumentation(t)}}},[e._v("Метод "+e._s(t.name))])])})),0),n("section",[n("div",{staticClass:"aboutElement"},[e.activeElement?n("div",{staticClass:"elementName"},[e._v(" "+e._s(e.activeElement.name))]):e._e(),e.activeElement?n("div",{staticClass:"elementInfo"},[e._v(" "+e._s(e.activeElement.description)+" "),n("br"),n("br"),e.activeElement.example?n("div",[e._v(e._s(e.activeElement.example))]):e._e()]):e._e()]),n("br"),n("br"),n("div",{staticClass:"funnyThings"},[e._v("Some funny things")])]),n("aside",[e._v(" Some fast addresses ")])])])},o=[function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("header",[n("div",[e._v("Документация Activae Vitae")])])}],s=n("3835"),a=(n("4fad"),n("e9c4"),n("a4d3"),n("e01a"),n("ac1f"),n("5319"),n("b0c0"),
[
    {
        id: 1,
        name:"/login POST",
        description:"Получение нового токена для пользователя. Его надо указывать заголовком Authorization: Basic <token>"
    },
    {
        id: 2,
        name:"/register POST",
        description:"Регистрация нового пользователя. Здесь передаётся пароль в открытом виде."
    },
    {
        id: 3,
        name:"/events GET",
        description:"Получение событий с указанными параметрами."
    },
    {
        id: 4,
        name:"/event GET",
        description:"Получение конкретного события по его ID."
    },
    {
        id: 5,
        name: "/event POST",
        description: "Добавление мероприятия."
    },
    {
        id: 6,
        name: "/event PATCH",
        description: "Внесение изменений в мероприятие. Обязателен только параметр id. Остальные необязательные."
    },
    {
        id: 7,
        name: "/event DELETE",
        description: "Удаление мероприятия."
    },
    {
        id: 9,
        name: "/event/save POST",
        description: "Сохранение определённого мероприятия."
    },
    {
       id: 10,
       name: "/event/save DELETE",
       description: "Убирает из сохранённых мероприятий."
    },
    {
        id: 11,
        name: "/event/rate PUT",
        description: "Устанавливает оценку за мероприятие. rate должен быть от -1 до 1 включительно."
    },
    {
        id: 12,
        name: "/event/rate GET",
        description: "Получение оценок мероприятия. rate возвращается в виде числа (от -1 до 1 включительно)."
    },
    {
        id: 13,
        name: "/my_events GET",
        description: "Возвращает сохранённые мероприятия."
    },
    {
        id: 14,
        name: "/own_events GET",
        description: "Возвращает созданные пользователем мероприятия."
    },
    {
        id: 15,
        name: "/verify POST",
        description: "Подтверждение стороннего аккаунта."
    },
    {
        id: 16,
        name: "/accounts GET",
        description: "Получение списка аккаунтов с рядом характеристик. offset - это смещение от начала списка; limit - максимальное количество объектов."
    },
    {
        id: 17,
        name: "/own_account PATCH",
        description: "Внесение изменений в профиль аккаунта."
    },
    {
        id: 18,
        name: "/account PATCH",
        description: "Внесение роли пользователя в системе."
    },
    {
        id: 19,
        name: "/comments GET",
        description: "Получение всех комментариев в системе."
    },
    {
        id: 20,
        name: "/comments POST",
        description: "Написание комментария."
    },
    {
        id: 21,
        name: "/comments DELETE",
        description: "Удаление комментария."
    }
]
),
c={
    "/login POST": {
        send: {
            email: "test@gmail.com",
            hash_password: "44jjJJj44JJrrtt..."
        },
        response: {
            code: 200,
            user_id: 1,
            full_name: "Some Test Values",
            role: "Director",
            verified: false,
            token: "233JJjrrddd555ccd4LLSSHhhshshaLss"
        }
    },
    "/register POST":{
        send: {
            full_name: "Some Test Values",
            password: "444gGGGGGhgfdd",
            email:"test@gmail.com",
            role:"Director"
        },
        response: {
            code: 200
        }
    },
    "/events GET": {
        send: {
            offset: 0,
            limit: 6,
            query: "event"
        },
        response: {
            code: 200,
            events: [
                {
                    id: 1,
                    name:"my event",
                    is_saved: !0,
                    short_description: "short event description",
                    date:"27.01.2022"
                },
                {
                    id: 2,
                    name: "my event 2 ",
                    is_saved: true,
                    short_description: "some long event description",
                    date: "29.01.2022"
                }
            ]
        }
    },
    "/event GET": {
        send: {
            id: 1
        },
        response: {
            code: 200,
            event: {
                id: 1,
                date:"27.01.2022 12:00",
                name: "my event",
                format: "Очно",
                description:"my full description for this thing...",
                photos:["https://imgur.com/333E","https://imgur.com/FFf54"]
            }
        }
    },
    "/event POST": {
        send: {
            name:"my new event",
            date:"28.01.2022 12:00",
            description: "full description of this thing...",
            short_description:"some short description...",
            format: "Очно",
            photos: "https://i.stack.imgur.com/1UKp7.png,https://www.dofactory.com/img/sql/sql-outer-joins.png"
        },
        response: {
            code: 200,
            event: {
                id: 1,
                date: '28.01.2022 12:00',
                short_description: 'some short description...',
                name: 'my new event'
            }
        }
    },
    "/event PATCH": {
        send: {
            id: 1,
            name: "My new name",
            short_description: "Some new short text",
            description: "Some new looong text",
            date: "10.03.2022 12:00",
            format: "Весёлый дистанционный",
            photos: "https://i.stack.imgur.com/1UKp7.png"
        },
        response: {
            code: 200
        }
    },
    "/event DELETE": {
        send: {
            id: 1
        },
        response: {
            code: 200
        }
    },
    "/event/save POST": {
        send: {
            id: 1
        },
        response: {
            code: 200
        }
    },
    "/event/save DELETE": {
        send: {
            id: 1
        },
        response: {
            code: 200
        }
    },
    "/event/rate PUT": {
        send: {
            id: 1,
            rate: 1
        },
        response: {
            code: 200
        }
    },
    "/event/rate GET": {
        send: {
            event_id: 1
        },
        response: {
            code: 200,
            rates: {
                "-1": 10,
                "0": 20,
                "1": 15
            }
        }
    },
    "/verify POST": {
        send: {
            user_id: 1
        },
        response: {
            code: 200
        }
    },
    "/accounts GET": {
        send: {
            limit: 10,
            offset: 0
        },
        response: {
            code: 200,
            users: [
                {
                    id: 1,
                    role: "director",
                    verified: !1,
                    email: "testMe@gmail.com",
                    full_name: "Testing Test"
                }
            ]
        }
    },
    "/own_account PATCH": {
        send: {
            role: "My new role",
            email: "testMe@gmail.com",
            full_name: "My New Brand Full Name"
        },
        response: {
            code: 200
        }
    },
    "/account PATCH": {
        send: {
            user_id: 1,
            role: "director"
        },
        response: {
            code: 200
        }
    },
    "/comments GET": {
        send: {
            event_id: 1
        },
        response: {
            code: 200,
            comments: [
                {
                    id: 133,
                    event_id: 1,
                    text: "Какое счастье иметь такое мероприятие!",
                    user_id: 1
                },
            ]
        }
    },
    "/comments POST": {
        send: {
            event_id: 1,
            text: "Какое счастье иметь такое мероприятие!"
        },
        response: {
            code: 200
        }
    },
    "/comments DELETE": {
        send: {
            id: 133
        },
        response: {
            code: 200
        }
    },
    "/my_events GET": {
        send: {
            limit: 10,
            offset: 0
        },
        response: {
            code: 200,
            events: [
                {
                    id: 2,
                    name: "my event 2",
                    is_saved: true,
                    short_description: "some long event description",
                    date: "29.01.2022"
                }
            ]
        }
    },
    "/own_events GET": {
        send: {
            limit: 10,
            offset: 0
        },
        response: {
            code: 200,
            events: [
                {
                    id: 2,
                    name: "my event 2",
                    is_saved: true,
                    short_description: "some long event description",
                    date: "29.01.2022"
                }
            ]
        }
    }
}
    ;console.log(c);var l={examples:c,documenation:a};function d(e){var t="Параметры отправления:\n",n="Ответ сервера:\n";if(!e)return"";for(var i=0,r=Object.entries(e.send);i<r.length;i++){var o=Object(s["a"])(r[i],2),a=o[0],c=o[1];t+="  "+a+": "+JSON.stringify(c)+"\n"}for(var l=0,d=Object.entries(e.response);l<d.length;l++){var p=Object(s["a"])(d[l],2),u=p[0],m=p[1];n+="  "+u+": "+JSON.stringify(m)+"\n"}return t+"\n\n\n"+n}var p={name:"App",data:function(){return{elementsList:l.documenation,activeElement:null,docsExample:l.examples,translitaration:d}},methods:{setValuesForDocumentation:function(e){var t=e.description,n=e;return t=t.replace("\n","<br />"),n.description=t,n.example=this.translitaration(this.docsExample[n.name]),this.activeElement=n,null}}},u=p,m=(n("d226"),n("2877")),v=Object(m["a"])(u,r,o,!1,null,null,null),f=v.exports;i["a"].config.productionTip=!1,new i["a"]({render:function(e){return e(f)},data:{}}).$mount("#app")},d226:function(e,t,n){"use strict";n("12c0")}});
//# sourceMappingURL=app.7ec63a80.js.map