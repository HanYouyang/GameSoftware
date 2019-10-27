class Cloud extends GuaImage {
    constructor(game){
        super(game, 'cloud')
        this.setup()
    }
    setup(){
        this.name = 'cloud'
        this.speed = 1
        this.x = randomBetween(0, 300)
        this.y = randomBetween(0, 10)
    }
    update(){
        this.y += this.speed
        if (this.y > 800){
            this.setup()
        }
    }
    debug(){
        this.speed = config.cloud_speed
    }
}
