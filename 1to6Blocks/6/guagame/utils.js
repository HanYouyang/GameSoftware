//调试基本工具
var log = console.log.bind(console)
var e = sel => document.querySelector(sel)
// var log = function(s){
//     e('#id-text-log').value += '\n' + s
// }
//简化函数的时候，首先要考虑如何把变量们变成一个对象
var imageFromPath = function(path){
    //给一个路径，载入一张图片，返回图片
    var img = new Image()
    img.src = path//注意图片格式可能出现各种内容
    return img
}
var rectIntersects = function(a, b) {
    var o = a
    //log('a, b', a, b)
    //log('o.image.height', o.image.height)
    // log('o.h', o.h)
    if (b.y > o.y && b.y < o.y + o.h) {
        if (b.x > o.x && b.x < o.x + o.w) {
            return true
        }
    }
    return false
}