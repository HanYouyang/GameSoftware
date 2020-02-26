class GuaLabel {
    constructor(game, text){
        this.game = game
        this.text = text
        this.x = 0
        this.y = 0
    }
    static new(game, text){
        return new this(game, text)
    }
    draw(){
        this.game.context.font = '20px serif'
        this.game.context.fillText(this.text, this.x, this.y)
    }
    update(){
    }
}