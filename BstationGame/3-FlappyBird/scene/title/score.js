class Score {
    constructor(game, text){
        this.game = game
        this.text = text

        this.x = 0
        this.y = 20
        this.font = 15
    }
    static new(game, text){
        return new this(game, text)
    }
    draw(){
        this.game.context.font = `${this.font}px serif`
        this.game.context.fillText(this.text, this.x, this.y)
    }
    update(){
        this.text = `积分 ${this.game.score}`
        this.game.context.fillText(this.text, this.x, this.y)
    }
}