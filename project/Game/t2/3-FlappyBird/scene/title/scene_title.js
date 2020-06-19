class SceneTitle extends GuaScene {
    constructor(game){
        super(game)
        this.pipePaused = false
        this.birdPaused = false

        var bg = GuaImage.new(game, 'bg')
        this.addElement(bg)

        this.game.score = 0
        var label = Score.new(game, '积分')
        this.addElement(label)

        this.pipe = Pipes.new(game)
        this.addElement(this.pipe)

        var bird = Birds.new(game)
        bird.x = 100
        bird.y = 210
        this.bird = bird
        this.addElement(bird)

        var grd = Grounds.new(game)
        for (var g of grd.grounds) {
            this.addElement(g)
        }

        this.setUpInputs()
    }

    //这里不能自己写有update，会覆盖其他内容
    update(){
        super.update()
        for (var e of this.elements) {
            if (e.name == 'pipes') {
                for (var p of e.pipes) {
                    if (this.bird.x == p.x) {
                        this.game.score += 50
                    }
                }
            }
        }
    }
    setUpInputs(){
        var self = this
        var b = this.bird
        this.game.registerAction('a', function(keyStatus){
            b.move(-2, keyStatus)
        })
        this.game.registerAction('d', function(keyStatus){
            b.move(2, keyStatus)
        })
        this.game.registerAction('j', function(keyStatus){
            b.jump()
        })
        this.game.registerAction('p', function(keyStatus){
            self.paused = true
        })
        this.game.registerAction('o', function(keyStatus){
            self.paused = false
        })
    }
}