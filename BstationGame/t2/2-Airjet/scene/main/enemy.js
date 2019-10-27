class Enemy extends GuaImage {
    constructor(game){
        var type = randomBetween(0, 7)
        var enemyName = 'enemy' + type
        super(game, enemyName)
        this.setup()
    }
    setup(){
        this.name = 'enemy'
        this.coolDown = 3
        this.speed = randomBetween(1, 3)
        this.x = randomBetween(0, 300)
        this.y = randomBetween(0, 100)
    }
    fire(){
        if (this.coolDown == 0) {
            this.coolDown = config.fire_coolDown

            var b = EnemyBullet.new(this.game)
            b.x = this.x + this.w / 2
            b.y = this.y
            this.scene.addElement(b)
        }
    }
    //碰撞检测
    aInb(x, x1, x2){
        return x >= x1 && x <= x2
    }
    collide(other){
        let a = this
        let b = other
        // log('a and b', a, b) 
        if ( this.aInb(a.x, b.x, b.x + b.w) || this.aInb(b.x, a.x, a.x + a.w) ) {
            if ( this.aInb(a.y, b.y, b.y + b.h) || this.aInb(b.y, a.y, a.y + a.h) ) {
                return true
            }
        }
        return false
    }
    update(){
        if (this.coolDown > 0) {
            this.coolDown -= 1
        }
        this.fire()
        this.speed = config.enemy_speed
        this.y += this.speed
        if (this.y > 800){
            this.setup()
        }

        for (let i = 0; i < this.scene.elements.length; i++) {
            let element = this.scene.elements[i]
            if ((element.name == 'player') && this.collide(element)) {
                this.scene.removeElement(element)
                this.scene.allEnemy.splice(1)

                let x = element.x
                let y = element.y
                let ps2 = GuaParticleSystem.new(this.scene.game, x, y)
                this.scene.addElement(ps2)
            }
        }

    }
}