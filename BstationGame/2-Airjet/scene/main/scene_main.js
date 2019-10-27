const config = {
    player_speed: 10,
    bullet_speed: 5,
    enemy_bullet_speed: 4,
    cloud_speed: 1,
    enemy_speed: 2,
    fire_coolDown: 10,
}

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
        // this.speed = config.bullet_speed
        this.y -= this.speed
        for (let i = 0; i < this.scene.elements.length; i++) {
            let element = this.scene.elements[i]
            if (element.name == 'enemy' && this.collide(element)) {
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
class enemyBullet extends GuaImage {
    constructor(game){
        super(game, 'bullet')
        this.setup()
    }
    setup(){
        this.name = 'enemy_bullet'
        this.speed = config.enemy_bullet_speed
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
        // this.speed = config.bullet_speed
        this.y += this.speed
        for (let i = 0; i < this.scene.elements.length; i++) {
            let element = this.scene.elements[i]
            if ((element.name == 'player'||element.name == 'player_bullet') && this.collide(element)) {
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

            var b = enemyBullet.new(this.game)
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

class Scene extends GuaScene {
    constructor(game){
        super(game)
        this.setup()
        this.setupInputs()
    }
    setup(){
        this.numberOfEnemy = 5
        this.allEnemy = []
        //读图部分和画图部分还是要分开，避免出现找不到资源
        var game = this.game
        this.bg = GuaImage.new(game, 'sky')
        this.cloud = Cloud.new(game)
        this.player = Player.new(game)//仍然需要注册事件
        this.player.x = 100
        this.player.y = 800

        this.addElement(this.bg)
        this.addElement(this.cloud)
        this.addElement(this.player)
        this.addEnemies()
    }
    addEnemies(){
        //初始化数量飞机
        for (let i = this.allEnemy.length; i < this.numberOfEnemy; i++) {
            const e = Enemy.new(this.game)
            this.allEnemy.push(e)
            this.addElement(e)
        }
        this.enemies = this.allEnemy
    }
    setupInputs(){
        var g = this.game
        var s = this
        g.registerAction('a', function(){
            s.player.moveLeft()//把注册的键位和更新的函数都确定了，而整个game对象内部都有监听所以可以直接行驶功能
        })
        g.registerAction('d', function(){
            s.player.moveRight()
        })
        g.registerAction('w', function(){
            s.player.moveUp()//把注册的键位和更新的函数都确定了，而整个game对象内部都有监听所以可以直接行驶功能
        })
        g.registerAction('s', function(){
            s.player.moveDown()
        })
        g.registerAction('j', function(){
            s.player.fire()
        })
    }
    update(){
        // super.update()
        if (this.allEnemy.length < this.numberOfEnemy) {
            const e = Enemy.new(this.game)
            this.allEnemy.push(e)
            this.addElement(e)
        }
        for (var element of this.elements) {
            element.update()
        }
    }
}