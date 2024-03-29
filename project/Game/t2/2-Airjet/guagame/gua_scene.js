class GuaScene {
    constructor(game){
        //在这里给出接口就好了，别的不用管了
        this.game = game
        this.elements = []
        this.debugModeEnabled = true
    }
    static new(game){
        var i = new this(game)
        return i
    }

    addElement(guaImage){
        guaImage.scene = this
        this.elements.push(guaImage)
    }
    removeElement(guaImage){
        guaImage.scene = this
        for (let i = 0; i < this.elements.length; i++) {
            let element = this.elements[i]
            if (element == guaImage) {
                this.elements.splice(i, 1)
            }
        }
    }

    draw(){//这里一定要被继承的函数必须有这个相应的内容
        for (var element of this.elements) {
            element.draw()
        }
    }

    update(){
        if (this.debugModeEnabled) {
            for (var i = 0; i < this.elements.length; i++) {
                var element = this.elements[i]
                //log('element', element)
                element.debug && element.debug()
            }
        }
        for (var element of this.elements) {
            element.update()
        }
    }
}