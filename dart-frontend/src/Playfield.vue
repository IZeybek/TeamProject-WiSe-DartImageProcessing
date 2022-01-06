<template>
    <div id="shootout">
        <div class="head">
            <div class="record">
                <v-btn @click="isHidden=true; debug()"> Correction</v-btn>
                <input v-if="isHidden" v-model ="correct" placeholder="Richtige zahl eingeben">
                <div @click="undo(correct);isHidden = false">{{ record[0] | totext }}</div>
                <div @click="undo();isHidden = true;">{{ record[1] | totext }}</div>
                <div @click="undo();isHidden = true">{{ record[2] | totext }}</div>
                <v-btn @click="isHidden=true; debug()">Failed</v-btn>
            </div>
        </div>
        <div class="players">
            <div v-for="(player, index) in players" v-bind:key="player.name" :class="{ active: turn === index, player }">
                <h3>{{ player.name }}</h3>
                <span class="score">{{ player.score }}</span>
            </div>
        </div>
        <div v-if="playerchange" class="playerchange" @click="changeplayer">Player change</div>
    </div>
</template>

<script>
export default {
    name: 'playfield',
    props: ['playernames', 'initialSconre'],
    data: function() {
        return{
            record:[], 
            serverscore:0,
            isHidden:false,
            players:[],
            correct:"",
            connection:null,
        }
    },
    filters:{
        totext(serverscore) {
            if (serverscore == 0) {
                return ''
            }
            if(serverscore == 0) {
                return serverscore
            }
        }
    },
    created() {
        this.init()
        this.createWebsocket()
    },
    methods: {
        init() {
            this.players = this.playernames.map(name => ({
                name,
                score: this.initialScore || 301,
                throws: [],
            }))
        },
        debug() {
            console.log(this.isHidden);
        },
        undo(correct) {
            // implement later
            console.log("life is good " + correct)
        },
        createWebsocket() {
            this.connection = new WebSocket("ws://127.0.0.1:6969");
            console.log(this.connection)
            this.connection.send("hello")
        }
    }
}
</script>

<style>
#shootout { display: relative }
.head {
  display: grid;
  grid-template-columns: 2fr 1fr;
  place-items: center;
  border: 5px solid black;
}

.players {
  display: flex;
  color: white;
}
.record {
  justify-self: end;
  background-color: rgb(173, 28, 28);
}

.record > div {
  color: white;
  font-weight: bold;
  font-size: 1rem;
  border: 2px solid white;
  padding: 10px;
  min-width: 150px;
  min-height: 45px;
}
.players > div {
  padding: 10px;
  border-left: 4px solid black;
  border-bottom: 4px solid black;
}.players > div:last-child {
  border-right: 4px solid black;
}
h3 {
  margin: 0 0 5px 0;
}
.score {
  margin-right: 10px;
}
.player {
  background-color: #333;
  flex-grow: 1;
}
.player.active:nth-child(1) {
  background-color: red;
}
.player.active:nth-child(2) {
  background-color: blue;
}
.player.active:nth-child(3) {
  background-color: green;
}
.player.active:nth-child(4) {
  background-color: purple;
}
.player.active:nth-child(5) {
  background-color: rgb(28, 114, 110);
}

.playerchange, .gameover {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 100%;
  font-weight: bold;
  transform: translate(-50%, -50%);
  background-color: rgb(189, 201, 87);
  color:white;
  font-size: 2rem;
  padding: 30px;
  cursor: pointer;
}
.gameover { padding: 0}
.gameover > div {padding: 30px}
.playagain {
  background-color: rgb(45, 102, 19);
}

</style>

