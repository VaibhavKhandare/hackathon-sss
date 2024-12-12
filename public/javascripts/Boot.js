export class Boot extends Phaser.Scene
{
    constructor ()
    {
        super('Boot');
    }

    preload ()
    {
        this.load.setBaseURL('https://cdn.phaserfiles.com/v385');
        //  The Boot Scene is typically used to load in any https://labs.phaser.io/assets you require for your Preloader, such as a game logo or background.
        //  The smaller the file size of the https://labs.phaser.io/assets, the better, as the Boot Scene itself has no preloader.

        this.load.image("preloader", "assets/games/coin-clicker/preloader.png");
    }

    create ()
    {
        //  A global value to store the highscore in
        this.registry.set('highscore', 0);

        this.scene.start('Preloader');

        // this.input.once('pointerdown', () => {

        //     this.scene.start('Preloader');

        // });
    }
}