class Player extends GuaImage {
    constructor(game){
        super(game, 'player')
        this.setup()
    }
    setup(){
        this.name = 'player'
        this.speed = 7
        this.coolDown = config.fire_coolDown
    }
    update(){
        this.speed = config.player_speed
        if (this.coolDown > 0) {
            this.coolDown -= 1
        }
    }
    moveLeft(){
        this.x -= this.speed
    }
    moveRight(){
        this.x += this.speed
    }
    moveUp(){
        this.y -= this.speed
    }
    moveDown(){
        this.y += this.speed
    }
    fire(){
        if (this.coolDown == 0) {
            this.coolDown = config.fire_coolDown

            var b = Bullet.new(this.game)
            b.x = this.x + this.w / 2
            b.y = this.y
            this.scene.addElement(b)
        }
    }
}