const CryptoJS = require("crypto-js");

let value = '{"o00o0o00o0o0o0":"eval0514undefined"}'; //待加密的字符串
let secret_value = "8f03e080ec3f9a5d"; //密匙 16位

// 密匙和向量处理
let secret = CryptoJS.enc.Utf8.parse(secret_value);

// 加密
let encrypted = CryptoJS.AES.encrypt(value, secret, {
    // mode 支持 CBC, CFB,CTB,ECB,OFB,OFB, 默认CBC
    mode: CryptoJS.mode.ECB,

    // NoPadding, zeropadding 默认Pkcs7 即 pkcs5
    padding: CryptoJS.pad.Pkcs7
});

// 将加密结果转换为字符串
encrypted = encrypted.toString();

console.log(encrypted);