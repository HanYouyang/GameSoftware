class Score {
    constructor(game, text){
        this.game = game
        this.text = text
    }
    static new(game, text){
        return new this(game, text)
    }
    draw(){
        this.game.context.font = '15px serif'
        // log('draw label', this.game, this.text)
        this.game.context.fillText(this.text, 0, 20)
    }
    update(){
        this.text = `积分：${this.scene.score}`
        this.game.context.fillText(this.text, 0, 20)
    }
}