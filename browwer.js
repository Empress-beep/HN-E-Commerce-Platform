delete __dirname
delete __filename

function get_enviroment(proxy_array) {
    for (var i = 0; i < proxy_array.length; i++) {
        handler = '{\n' +
            '    get: function(target, property, receiver) {\n' +
            '        console.log("方法:", "get  ", "对象:", ' +
            '"' + proxy_array[i] + '" ,' +
            '"  属性:", property, ' +
            '"  属性类型:", ' + 'typeof property, ' +
            // '"  属性值:", ' + 'target[property], ' +
            '"  属性值类型:", typeof target[property]);\n' +
            'if(typeof target[property] === "undefined"){debugger}' +
            '        return target[property];\n' +
            '    },\n' +
            '    set: function(target, property, value, receiver) {\n' +
            '        console.log("方法:", "set  ", "对象:", ' +
            '"' + proxy_array[i] + '" ,' +
            '"  属性:", property, ' +
            '"  属性类型:", ' + 'typeof property, ' +
            // '"  属性值:", ' + 'target[property], ' +
            '"  属性值类型:", typeof target[property]);\n' +
            '        return Reflect.set(...arguments);\n' +
            '    }\n' +
            '}'
        eval('try{\n' + proxy_array[i] + ';\n'
            + proxy_array[i] + '=new Proxy(' + proxy_array[i] + ', ' + handler + ')}catch (e) {\n' + proxy_array[i] + '={};\n'
            + proxy_array[i] + '=new Proxy(' + proxy_array[i] + ', ' + handler + ')}')
    }
}

proxy_array = ['window', 'document', 'location', 'navigator', 'history', 'screen', 'script', 'script.parentElement', 'meta']

setTimeout = function (){}
setInterval = function (){}

// window
window = global;
self=top=window;
window.ActiveXObject = undefined;
window.localStorage = {};
window.sessionStorage = {};
window.name = '';
window.addEventListener = function(args){
    console.log('调用了window的addEventListener函数的参数：', args)
}

script = {
    getAttribute: function (args){
        console.log('调用了document的getElementsByTagName的getAttribute的参数：', args)
        if (args === 'r'){
            return 'm'
        }
    },
    parentElement: {
        removeChild: function (args){
            console.log('调用了document的getElementsByTagName的parentElement的参数：', args)
        }
    }
}

meta = {
    getAttribute: function (args){
        console.log('调用了document的getElementsByTagName的getAttribute的参数：', args)
        if (args === 'r'){
            return 'm'
        }
    },
    parentNode: {
        removeChild: function (args){
            console.log('调用了document的getElementsByTagName的parentElement的参数：', args)
        }
    },
    content: 'content1'
}

// document
document = {
    createElement: function (args) {
        console.log('调用了document的createElement函数的参数：',args)
        if (args === 'div'){
            return {
                getElementsByTagName: function (args){
                    console.log('调用了document的createElement的getElementsByTagName函数的参数：',args)
                    if (args === 'i'){
                        return []
                    }
                }
            }
        }
        if (args === 'form'){
            return {}
        }
    },
    getElementsByTagName: function(args){
        console.log('调用了document的getElementsByTagName函数的参数：', args)
        if (args === 'script'){
            return [script,script];
        }
        if (args === 'meta'){
            return [meta,meta]
        }
        if (args === 'base'){
            return []
        }
    },
    appendChild: function (args){
        console.log('调用了document的appendChild函数的参数：',args)
    },
    removeChild: function (args){
        console.log('调用了document的removeChild函数的参数：',args)
    },
    addEventListener: function (args){
        console.log('调用了document的addEventListener函数的参数：', args)
    },
    getElementById: function (args){
        console.log('调用了document的getElementById函数的参数：', args)
    },
    'visibilityState' : 'visible',
    'cookie': ''
}

location = {
    "ancestorOrigins": {},
    "href": "https://ec.chng.com.cn/channel/home/#/purchase?top=0",
    "origin": "https://ec.chng.com.cn",
    "protocol": "https:",
    "host": "ec.chng.com.cn",
    "hostname": "ec.chng.com.cn",
    "port": "",
    "pathname": "/channel/home/",
    "search": "",
    "hash": "#/purchase?top=0"
}

navigator = {
    appCodeName : "Mozilla",
    appName : "Netscape",
    appVersion : "5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36 Edg/145.0.0.0",
    userAgent : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36 Edg/145.0.0.0",
    platform : "Win32"
}

get_enviroment(proxy_array)

// td代码
"ts_code"

// js代码
"fun_code"

function get_cookie(){
    return document.cookie
}