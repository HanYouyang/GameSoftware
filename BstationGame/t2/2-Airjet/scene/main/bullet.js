class Bullet extends GuaImage {
    constructor(game){
        super(game, 'bullet')
        this.setup()
    }
    setup(){
        this.name = 'player_bullet'
        this.speed = config.bullet_speed
        // this.speed = 1
        this.killed = false
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
        if (this.y < 0) {
            return
        }
        this.y -= this.speed

        for (let i = 0; i < this.scene.elements.length; i++) {
            let element = this.scene.elements[i]
            if (( element.name == 'enemy' || element.name == 'enemy_bullet') && this.collide(element)) {
                this.scene.removeElement(element)

                if (element.name == 'enemy') {
                    log('element.number', element.number)
                    for (let j = 0; j < this.scene.allEnemy.length; j++) {
                        let e = this.scene.allEnemy[j]
                        if (element.number == e.number) {
                            log('e.number', e.number)
                            this.scene.allEnemy.splice(j)
                        }
                    }
                }

                let x = element.x
                let y = element.y
                let ps2 = GuaParticleSystem.new(this.scene.game, x, y)
                this.scene.addElement(ps2)
            }
        }
    }
}
