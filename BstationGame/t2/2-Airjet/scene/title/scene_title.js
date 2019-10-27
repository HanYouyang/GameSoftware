class SceneTitle extends GuaScene {
    constructor(game){
        super(game)
        var label = GuaLabel.new(game, 'hello')
        this.addElement(label)

        var ps = GuaParticleSystem.new(game)
        log('ps', ps)
        this.addElement(ps)
    }
    //这里不能自己写有update，会覆盖其他内容
}