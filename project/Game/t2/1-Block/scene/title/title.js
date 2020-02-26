class SceneTitle extends GuaScene {
    constructor(game){
        super(game)
        game.registerAction('k', function(){
            var gameStart = Scene(game)
            game.replaceScene(gameStart)
        })

    }

    draw(){
        this.game.context.font = '30px serif'
        this.game.context.fillText('按 k 开始游戏', 90, 600)
    }

    update(){
        
    }

}