class SceneEnd extends GuaScene {
    constructor(game){
        super(game)

        var bg = GuaImage.new(game, 'bg')
        this.addElement(bg)

        var over = GuaImage.new(game, 'over')
        over.x = 20
        over.y = 100
        this.addElement(over)

        var bird = Birds.new(game)
        bird.x = 100
        bird.y = 435
        this.bird = bird
        this.addElement(bird)

        this.skipCount = 4
        this.grounds = []
        for (let i = 0; i < 25; i++) {
            var g = GuaImage.new(game, 'ground')
            g.x = i * 19
            g.y = 462
            g.name = 'ground'
            this.addElement(g)
            this.grounds.push(g)          
        }

        this.pipePaused = false
        this.birdPaused = true


        game.registerAction('r', function(){
            var gameRe = SceneGo.new(game)
            game.replaceScene(gameRe)
        })


        var label = GuaLabel.new(game, '按 r 重新开始游戏')
        label.x = 60
        label.y = 290
        this.addElement(label)

        var scoreLabel = Score.new(game, '积分')
        scoreLabel.x = 60
        scoreLabel.y = 250
        scoreLabel.font = 20
        this.addElement(scoreLabel)

    }

}