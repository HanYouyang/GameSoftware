class GuaGame{
    constructor(fps, images, runCallback){
        window.fps = fps
        this.images = images
        this.runCallback = runCallback

        this.scene = null
        this.actions = {}
        this.keydowns = {}

        this.canvas = document.querySelector('#id-canvas')
        this.context = this.canvas.getContext('2d')

        var self = this
        window.addEventListener('keydown', function(event){
            self.keydowns[event.key] = true
            //陷阱在于self此时不能和this一样,你此时不明确this到底是谁
            //在一段区域内提前指定好self等于this之后再进行选择
        })
        window.addEventListener('keyup', function(event){
            self.keydowns[event.key] = false
        })
        this.init()//初始化全部内容的启动就在这里了
        //下面的start是载入静态内容和开始动态内容分界
    }

    static instance(...args){
        this.i = this.i || new this(...args)//为什么这里用的是this.i
        return this.i
    }

    drawImage(img){
        this.context.drawImage(img.image, img.x, img.y)
    }
    registerAction(key, callback){
        this.actions[key] = callback
    }
    update(){
        //其实game里面的update和draw都没必要存在，因为这两个函数都调用scene的内容
        this.scene.update()
    }
    draw(){
        this.scene.draw()
    }
    runloop(){
        var g = this
        //调用当前已注册事件
        var actions = Object.keys(g.actions)//将对象的对应key转化为数组
        for (let i = 0; i < actions.length; i++) {
            let key = actions[i]
            // log('key', key)
            //依次遍历自己现在的内容从而让自己能够使用
            //log('g.actions[key]', g.actions[key])
            //log('g.actions[key]()', g.actions[key]())
            if (g.keydowns[key]){
                //如果按键被按下调用注册的action
                g.actions[key]()
            }
        }
        //update
        g.update()//最后的update是完全和整个监听按键分离开了，这个和操作与本来的不用关系了
        //clear
        g.context.clearRect(0, 0, g.canvas.width, g.canvas.height)
        //draw
        g.draw()
        //g.run()
        setTimeout(function(){
            g.runloop()
        }, 1000/(window.fps+1))//通过+1避免出现除以0
    }

    init(){
        //主要功能是载入图片
        var g = this
        var loads = []
        var names = Object.keys(g.images)
        for (let i = 0; i < names.length; i++) {
            let name = names[i]
            let path = g.images[name] //这里的变量在for里面使用块极作用域实际上是对自己非常好的一种方式，能够让自己的
            let img = new Image()
            img.src = path
            img.onload = function(){
                g.images[name] = img
                loads.push(1)
                if (loads.length == names.length) {
                    log('load images全部图片结束')
                    g.start()
                }
            }
        }
    }

    imageByName(name){
        //与init载入图片一起获得图片路径
        var g = this
        var img = g.images[name]
        var image = {
            w: img.width,
            h: img.height,
            images: img,
        }
        //log('image.now', image)
        return image
    }
    runWithScene(scene){
        //在外部调用，把scene加载到game里面，但这在game给到scene之后初始化scene
        var g = this
        g.scene = scene
        setTimeout(function(){
            // log('执行runloop前')
            g.runloop()
            // log('执行runloop后')
        }, 1000/(window.fps+1))//通过+1避免出现除以0
    }
    replaceScene(rep){
        //给一个外部能够调用的函数更改game的scene
        var g = this
        g.scene = rep
    }
    start(){
        //加载完图片后给出内部启动运行的功能，所以放在加载完图片后再调出顺序启动
        //但是这个顺序和callback都是自动进行的，加上scene都是手动进行的
        var g = this
        g.runCallback(g)//首次运行要有生成的内容
        //为的是给回调和函数里面的所有内容一个初始化生成的空间
    }
}
