class GuaParticle extends GuaImage {
    constructor(game){
        // this.game = game
        super(game, 'fire')
        this.setup()
    }
    setup(){
        this.life = 5
    }
    init(x, y, vx, vy){
        this.x = x
        this.y = y
        this.vx = vx
        this.vy = vy
    }
    update(){
        this.life --
        this.x += this.vx
        this.y += this.vy
        var factor = 0.1
        this.vx += factor * this.vx
        this.vy += factor * this.vy
    }

}