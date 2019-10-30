class SceneGo extends GuaScene {
    constructor(game){
        super(game)

        var bg = GuaImage.new(game, 'bg')
        this.addElement(bg)

        var ready = GuaImage.new(game, 'ready')
        ready.x = 45
        ready.y = 30
        this.addElement(ready)

        var bird = Birds.new(game)
        bird.x = 100
        bird.y = 230
        this.bird = bird
        this.addElement(bird)

        var grd = Grounds.new(game)
        for (var g of grd.grounds) {
            this.addElement(g)
        }

        this.pipePaused = false
        this.birdPaused = true

        var label = GuaLabel.new(game, '按 G 重新开始游戏')
        label.x = 60
        label.y = 290
        this.addElement(label)
        var label2 = GuaLabel.new(game, '按 J 向上跳跃')
        label2.x = 60
        label2.y = 320
        this.addElement(label2)

        game.registerAction('g', function(){
            var gameRe = SceneTitle.new(game)
            game.replaceScene(gameRe)
        })
    }

    // update(){
        
    // }

}