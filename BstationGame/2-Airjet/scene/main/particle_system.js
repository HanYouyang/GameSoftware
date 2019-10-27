class GuaParticleSystem {
    constructor(game, x, y){
        this.game = game
        this.setup(x, y)
    }
    setup(x, y){
        this.duration = 50
        this.x = x
        this.y = y
        this.numberOfParticles = 80
        this.particles = []
    }
    static new(game, x, y){
        return new this(game, x, y)
    }
    update(){
        this.duration --
        
        //添加小火花
        if (this.particles.length < this.numberOfParticles) {
            var p = GuaParticle.new(this.game)
            var s = 10
            var vx = randomBetween(-s, s)
            var vy = randomBetween(-s, s)
            p.init(this.x, this.y, vx, vy)
            this.particles.push(p)
        }
        //更新所有的小火花
        for (var p of this.particles) {
            p.update()
        }
        //删除死掉的小火花
        this.particles = this.particles.filter(p => p.life > 0)
    }
    draw(){
        if (this.duration < 0) {
            //应该从scene 中删除
            return
        }
        for (var p of this.particles) {
            p.draw()
        }
    }

}