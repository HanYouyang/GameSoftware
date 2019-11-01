class Grounds {
    //专门抽象成为一个元素，减轻循环负担，但是现在先不
    constructor(game){
        this.game = game

        this.name = 'grounds'
        this.skipCount = 4
        this.offset = -2

        this.grounds = []

        this.setup()

    }
    static new(game){
        return new this(game)
    }
    setup(){
        for (let i = 0; i < 25; i++) {
            var g = GuaImage.new(this.game, 'ground')
            g.x = i * 19
            g.y = 462
            g.name = 'ground'
            // this.addElement(g)
            this.grounds.push(g)          
        }
    }

    update(){
        this.skipCount --
        if (this.skipCount == 0) {
            this.skipCount = 4
            this.offset = 6
        }
        for (let i = 0; i < 25; i++) {
            var g = this.grounds[i]
            g.x += this.offset      
        }
    }
}
