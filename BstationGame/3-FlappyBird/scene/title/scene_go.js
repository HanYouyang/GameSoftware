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

        game.registerAction('g', function(){
            var gameRe = SceneTitle.new(game)
            game.replaceScene(gameRe)
        })
    }

    // update(){
        
    // }

}