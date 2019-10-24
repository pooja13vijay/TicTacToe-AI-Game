var app = new Vue({
  el: "#app",
  data: {
    grid_size: 4,
    squares: Array(9).fill(-1),
    player: ["circle-outline", "close"],
    additional_player: ["close", "circle-outline", "access-point", "account", "account-badge", "checkbox-blank-circle", "all-inclusive", "brightness-5", "camera-iris", "check", "checkbox-blank", "checkbox-blank-outline", "checkbox-intermediate", "chef-hat", "chess-bishop", "chess-king", "chess-knight", "chess-pawn", "chess-queen", "chess-rook", "circle-slice-8", "cloud", "dna", "emoticon-excited-outline", "emoticon-happy-outline", "emoticon-excited", "emoticon-happy", "emoticon-devil", "emoticon-devil-outline", "face"],
    chosen_additional_player: "",
    currentplayer: null,
    winning_player: [],
    choosing_player: false,
    setting_player: false,
    additional_rule: true,
    tie: false,
    player_settings: ['', ''],
    ai_players: [],
    log: []
  },
  computed: {
    endGame: function () {
      return this.squares.filter(x => x == -1).length == 0;
    },
    game_info: function () {
      let gi = {};
      this.player_settings.forEach((x,i) => {
        gi[`Player ${i}`] = `<span class="mdi mdi-${this.player[i]}"></span>&nbsp;${x ? x : 'human'}`;
      });
      gi["Game board"] = `[${this.squares}]`;
      gi["Current player"] = `${this.currentplayer} (<span class="mdi mdi-${this.player[this.currentplayer]}"></span>)`;
      return gi;
    }
  },
  mounted: function() {
    this.clearBoard();
    this.getAiList();
  },
  methods: {
    triggerStart: function () {
      currentplayer_name = this.player_settings[this.currentplayer];
      this.log.push(`Trigger Player ${this.currentplayer} (${ currentplayer_name == '' ? 'human' : currentplayer_name }) to start`);
      if (currentplayer_name != '') {
        this.callAiPlayer(currentplayer_name, this.currentplayer)
        .then(r => {
          if (r.error) {// || r.board_state.some((x,i) => x != this.squares[i])) {
            console.log(`error: move was called at ${r.board_state} but found ${this.squares} at move returned`)
          } else {
            this.fillAndSwitch(r.move);
          }
        })
      } else {
        this.log.push("Human player, please make your move");
      }
    },
    fill: function(i) {
      this.$set(this.squares, i, this.currentplayer);
      this.log.push(`Player ${this.currentplayer} filled square ${i}`);
      // this.log.push(`Board status: [${this.squares}]`);
    },
    switchPlayer: function() {
      if (this.winning_player.length == 0) {
        this.currentplayer = (this.currentplayer + 1) % this.player.length;
        currentplayer_name = this.player_settings[this.currentplayer];
        this.log.push(`Waiting for Player ${this.currentplayer} (${ currentplayer_name == '' ? 'human' : currentplayer_name })`);
        if (currentplayer_name != '') {
          this.callAiPlayer(currentplayer_name, this.currentplayer)
          .then(r => {
            if (r.error) {// || r.board_state.some((x,i) => x != this.squares[i])) {
              console.log(`error: move was called at ${r.board_state} but found ${this.squares} at move returned`)
            } else {
              this.fillAndSwitch(r.move);
            }
          })
        }
      }
    },
    fillAndSwitch: function(i) {
      if (this.winning_player.length == 0) {
        this.fill(i);
        let player_status = [...Array(this.player.length).keys()].map(this.checkPlayer);
        this.winning_player = player_status.filter(x => x.won);
        if (this.winning_player.length <= 0) {
          if (!this.endGame)
            this.switchPlayer();
          else {
            this.log.push(`All squares are occupied`);
            player_status = this.finalCheck();
            this.winning_player = player_status.filter(x => x.won);
            if (this.winning_player.length <= 0) {
              this.tie = true;
              this.log.push(`The two players tie`);
            } else {
              this.log.push(`Player ${this.winning_player[0].n} won with game board [${this.squares}]`);
            }
          }
        } else {
          this.log.push(`Player ${this.winning_player[0].n} won with game board [${this.squares}]`);
        }
      }
    },
    clearBoard: function() {
      this.squares = Array(this.grid_size**2).fill(-1);
      this.winning_player = [];
      this.currentplayer = 0;
      this.tie = false;
      this.log.push(`The game board is reset`);
    },
    checkPlayer: function(n) {
      let player_loc = this.squares.map((x,i) => (x == n) ? i : -1).filter(x => x > -1);
      let won = false;
      let winning = [];
      player_loc.forEach((x,i,arr) => {
        if ((!won) && (x % this.grid_size == 0)) {
          won = [...Array(this.grid_size).keys()].map(ti => arr.includes(x+ti)).every(avail => avail);
          winning = won ? [...Array(this.grid_size).keys()].map(ti => x+ti) : [];
        }

        if ((!won) && ([...Array(this.grid_size).keys()].includes(x))) {
          won = [...Array(this.grid_size).keys()].map(ti => arr.includes(x+ti*this.grid_size)).every(avail => avail);
          winning = won ? [...Array(this.grid_size).keys()].map(ti => x+ti*this.grid_size) : [];
        }

        if ((!won) && (x == 0)) {
          won = [...Array(this.grid_size).keys()].map(ti => arr.includes(x+ti*this.grid_size+ti)).every(avail => avail);
          winning = won ? [...Array(this.grid_size).keys()].map(ti => x+ti*this.grid_size+ti) : [];
        }

        if ((!won) && (x == this.grid_size-1)) {
          won = [...Array(this.grid_size).keys()].map(ti => arr.includes(x+ti*this.grid_size-ti)).every(avail => avail);
          winning = won ? [...Array(this.grid_size).keys()].map(ti => x+ti*this.grid_size-ti) : [];
        }
      });
      return { n: n, won: won, winning: winning, rule: 'original' };
    },
    addPlayer: function () {
      if (this.chosen_additional_player) {
        this.player.push(this.chosen_additional_player);
        this.choosing_player = false;
        this.clearBoard();
      }
    },
    changeGrid: function (n) {
      this.grid_size = Math.max(this.grid_size + n, 3);
      this.clearBoard();
    },
    finalCheck: function () {
      if (this.additional_rule) {
        let checks = [];
        [...Array(this.grid_size).keys()].forEach(x => {
          // add columns
          checks.push([...Array(this.grid_size).keys()].map(y => x + y*this.grid_size));
          // add rows
          checks.push([...Array(this.grid_size).keys()].map(y => x*this.grid_size + y));
          // add nw-se diagonal
          if (x == 0)
            checks.push([...Array(this.grid_size).keys()].map(y => x + y*this.grid_size + y));
          // add ne-sw diagonal
          if (x == this.grid_size - 1)
            checks.push([...Array(this.grid_size).keys()].map(y => x + y*this.grid_size - y));
        });
        let player_getting_line = checks.map(c => {
          let this_line = this.squares.filter((x,i) => c.includes(i));
          let result = this_line.reduce((acc, cValue) => {
            if (cValue > -1) acc[cValue] += 1;
            return acc;
          }, Array(this.player.length).fill(0));
          let maxCount = Math.max(...result);
          if (result.indexOf(maxCount) == result.lastIndexOf(maxCount)) return result.indexOf(maxCount);
          else return -1;
        });
        let player_points = player_getting_line.reduce((acc, cValue) => {
          if (cValue > -1) acc[cValue] += 1;
          return acc;
        }, Array(this.player.length).fill(0));
        console.log(player_points);
        player_points.forEach((x,i) => {
          this.log.push(`Player ${i} has ${x} points`)
        });
        let max_pp = Math.max(...player_points);
        if (player_points.indexOf(max_pp) == player_points.lastIndexOf(max_pp))
          return [...Array(this.grid_size).keys()].map(n => ({
            n: n,
            won: player_points.indexOf(max_pp) == n,
            winning: player_points,
            rule: 'additionals'
          }));
        else 
          return [...Array(this.grid_size).keys()].map(n => ({
            n: n,
            won: false,
            winning: player_points,
            rule: 'additionals'
          }));
      } else {
        return [];
      }
    },
    setPlayerHuman: function(n) {
      this.$set(this.player_settings, n, '');
    },
    setPlayer: function(n, p) {
      this.$set(this.player_settings, n, p);
      return this.initAiPlayer(p);
    },
    getAiList: function() {
      const request = new Request('./get-ai-players');
      return fetch(request)
      .then(r => r.json())
      .then(r => {
        this.ai_players = r;
      });
    },
    initAiPlayer: function(name) {
      const request = new Request(`./init-ai-player/${name}`);
      return fetch(request)
      .then(r => r.json())
      .then(console.log);
    },
    getInitAiPlayers: function () {
      const request = new Request(`./get-init-ai-players`);
      return fetch(request)
      .then(r => r.json())
      .then(console.log);
    },
    callAiPlayer: function (name, n) {
      const request = new Request(`./call-ai-player/${name}/${this.squares}/${n}`);
      return fetch(request)
      .then(r => r.json())
      .then(r => {
        console.log(r);
        return r;
      });
    }
  }
})
