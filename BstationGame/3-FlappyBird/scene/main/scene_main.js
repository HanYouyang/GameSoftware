// const config = {
//     player_speed: 10,
//     bullet_speed: 5,
//     cloud_speed: 1,
//     enemy_speed: 5,
//     fire_coolDown: 10,
// }

class Scene extends GuaScene {
    constructor(game){
        super(game)
        this.setup()
        this.setupInputs()
    }
    setup(){
        this.numberOfEnemy = 10
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
        //log('elements1', this.elements)
        this.addEnemies()

        var ps = GuaParticleSystem.new(this.game)
        this.addElement(ps)
    }
    addEnemies(){
        var allEnemy = []
        for (let i = 0; i < this.numberOfEnemy; i++) {
            const e = Enemy.new(this.game)
            allEnemy.push(e)
            this.addElement(e)
        }
        this.enemies = allEnemy
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
        super.update()
        this.cloud.y += 1
    }

}