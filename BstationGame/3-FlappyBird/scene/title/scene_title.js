class SceneTitle extends GuaScene {
    constructor(game){
        super(game)

        var bg = GuaImage.new(game, 'bg')
        this.addElement(bg)

        this.score = 0
        var label = Score.new(game, '目前积分')
        this.addElement(label)

        this.pipe = Pipes.new(game)
        this.addElement(this.pipe)

        var bird = Birds.new(game)
        bird.x = 100
        bird.y = 230
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

        this.paused = false
        this.setUpInputs()
        // log('this.elements', this.elements)
    }

    //这里不能自己写有update，会覆盖其他内容
    update(){
        super.update()
        this.skipCount --
        var offset = -2
        if (this.skipCount == 0) {
            this.skipCount = 4
            offset = 6
        }
        for (let i = 0; i < 25; i++) {
            var g = this.grounds[i]
            g.x += offset      
        }
        for (var e of this.elements) {
            if (e.name == 'pipes') {
                for (var p of e.pipes) {
                    if (this.bird.x == p.x) {
                        this.score += 50
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