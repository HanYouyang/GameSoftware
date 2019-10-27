const config = {
    player_speed: 10,
    bullet_speed: 5,
    enemy_bullet_speed: 4,
    cloud_speed: 1,
    enemy_speed: 2,
    fire_coolDown: 10,
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