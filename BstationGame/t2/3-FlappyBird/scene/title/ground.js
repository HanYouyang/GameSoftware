class Grounds extends GuaImage{

    //专门抽象成为一个元素，减轻循环负担，但是现在先不
    constructor(game){
        super(game, enemyName)
        this.setup()
        this.name = 'ground'

        for (let i = 0; i < this.columsOfPipes; i++) {
            var p1 = GuaImage.new(game, 'pipe')
            p1.flipY = true
            p1.x = 250 + (i + 3) * this.wideSpace
            log('p1.x now', p1.x)
            var p2 = GuaImage.new(game, 'pipe')
            p2.x = p1.x
            this.resetPipePosition(p1, p2)
            this.pipes.push(p1)
            this.pipes.push(p2)
        }
    }
    static new(game){
        return new this(game)
    }

    update(){
        for (let i = 0; i < this.pipes.length / 2; i += 2) {
            var p1 = this.pipes[i]
            var p2 = this.pipes[i + 1]
            p1.x -= 2
            p2.x -= 2
            // log('p2.x now', p2.x)
            if (p1.x < -100){
                p1.x += this.wideSpace * this.columsOfPipes
            }
            if (p2.x < -100){
                p2.x += this.wideSpace * this.columsOfPipes
                this.resetPipePosition(p1, p2)
                // log('p1.x, p2.x', p1.x, p2.x)
            }
            // 这里的双管子而非三管子问题一直存在
        }
    }
    draw(){
        // 全部继承自guaAnimation的draw
        var context = this.game.context 
        for (var p of this.pipes){
            //下面代码来自stack
            context.save()
            // log('this.x', this.x)

            var w2 = p.w / 2
            var h2 = p.h / 2
            context.translate(p.x + w2, p.y + h2)
            var scaleX = p.flipx ? -1 : 1
            var scaleY = p.flipY ? -1 : 1
            context.scale(scaleX, scaleY)
            context.rotate(p.rotation *  Math.PI / 180)
            context.translate(-w2, -h2)

            context.drawImage(p.texture, 0, 0)

            context.restore()
        }

    }
}
