from enum import Enum, IntEnum
from dataclasses import dataclass, field
from typing import Optional, List, Union, Tuple, Dict

class PokerRound(Enum):
    PRE_FLOP = 'pre-flop'
    FLOP = 'flop'
    TURN = 'turn'
    RIVER = 'river'
    SHOWDOWN = 'showdown'

PlayerID = str

class Rank(IntEnum):
    ACE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13

class Suit(Enum):
    HEARTS = 'hearts'
    DIAMONDS = 'diamonds'
    CLUBS = 'clubs'
    SPADES = 'spades'

@dataclass
class Card:
    rank: Rank
    suit: Suit

    def __str__(self):
        return f"{self.rank.name.capitalize()} of {self.suit.name.capitalize()}"

@dataclass
class PokerPlayer:
    id: PlayerID
    stack: int
    folded: bool
    current_bet: int
    last_round: Optional[PokerRound] = None

    def __str__(self):
        return (
            f"Player {self.id}: Stack: {self.stack}, "
            f"Folded: {self.folded}, Current Bet: {self.current_bet}, "
            f"Last Round: {self.last_round.value if self.last_round else 'None'}"
        )

@dataclass
class PokerConfig:
    dealer_position: int
    small_blind: int
    big_blind: int
    max_players: int

    def __str__(self):
        return (
            f"PokerConfig: Dealer Position: {self.dealer_position}, "
            f"Small Blind: {self.small_blind}, Big Blind: {self.big_blind}, "
            f"Max Players: {self.max_players}"
        )

@dataclass
class PokerSharedState:
    dealer_position: int
    small_blind: int
    big_blind: int
    pot: int
    target_bet: int
    players: List[PokerPlayer]
    round: PokerRound
    done: bool
    cards: List[Card]
    whose_turn: Optional[PlayerID] = None

    def __str__(self):
        player_info = "\n".join(f"  {p}" for p in self.players)
        community_cards = " ".join(str(card) for card in self.cards) if self.cards else "None"
        
        return (
            f"PokerSharedState:\n"
            f"  Dealer Position: {self.dealer_position}\n"
            f"  Small Blind: {self.small_blind}\n"
            f"  Big Blind: {self.big_blind}\n"
            f"  Pot: {self.pot}\n"
            f"  Target Bet: {self.target_bet}\n"
            f"  Round: {self.round.value}\n"
            f"  Done: {self.done}\n"
            f"  Whose Turn: {self.whose_turn if self.whose_turn else 'None'}\n"
            f"  Community Cards: {community_cards}\n"
            f"  Players:\n{player_info}"
        )

@dataclass
class PokerGame:
    state: PokerSharedState
    config: PokerConfig
    hands: Dict[PlayerID, Tuple[Card, Card]]
    deck: List[Card]

    def __str__(self):
        hands_info = "\n".join(f"  {pid}: {hand[0]}, {hand[1]}" for pid, hand in self.hands.items())
        deck_info = ", ".join(str(card) for card in self.deck)
        
        return (
            f"PokerGame:\n"
            f"{self.config}\n"
            f"{self.state}\n"
            f"  Hands:\n{hands_info}\n"
            f"  Deck: {deck_info}"
        )

GameLog = List[str]

class ActionType(Enum):
    RAISE = 'raise'
    FOLD = 'fold'
    CALL = 'call'

@dataclass
class Action:
    type: ActionType
    amount: Optional[int] = None

    def __str__(self):
        return f"Action: {self.type.value} {self.amount if self.amount else ''}".strip()

@dataclass
class ClientMessage:
    type: str
    action: Optional[Action] = None

    def __str__(self):
        return f"ClientMessage: Type: {self.type}, Action: {self.action if self.action else 'None'}"

class ServerUpdateMessageType(Enum):
    GAME_STARTED = 'game-started'
    PLAYER_JOINED = 'player-joined'
    PLAYER_LEFT = 'player-left'
    ACTION = 'action'
    GAME_ENDED = 'game-ended'

@dataclass
class ServerUpdateMessage:
    type: ServerUpdateMessageType
    action: Optional[Action] = None
    player: Optional[PokerPlayer] = None
    players: Optional[List[PokerPlayer]] = None
    payouts: Optional[Dict[str, int]] = None
    reason: Optional[str] = None

    def __str__(self):
        players_info = ", ".join(str(p) for p in self.players) if self.players else "None"
        payouts_info = ", ".join(f"{k}: {v}" for k, v in self.payouts.items()) if self.payouts else "None"

        return (
            f"ServerUpdateMessage:\n"
            f"  Type: {self.type.value}\n"
            f"  Action: {self.action if self.action else 'None'}\n"
            f"  Player: {self.player if self.player else 'None'}\n"
            f"  Players: {players_info}\n"
            f"  Payouts: {payouts_info}\n"
            f"  Reason: {self.reason if self.reason else 'None'}"
        )

@dataclass
class ServerStateMessage:
    client_id: str
    username: str
    game_state: Optional[PokerSharedState] = None
    hand: Optional[Tuple[Card, Card]] = None
    in_game_players: List[PokerPlayer] = field(default_factory=list)
    spectator_players: List[PokerPlayer] = field(default_factory=list)
    queued_players: List[PokerPlayer] = field(default_factory=list)
    players: List[PokerPlayer] = field(default_factory=list)
    last_updates: List[ServerUpdateMessage] = field(default_factory=list)

    def __str__(self):
        in_game_players_info = "\n".join(str(p) for p in self.in_game_players)
        spectator_players_info = "\n".join(str(p) for p in self.spectator_players)
        queued_players_info = "\n".join(str(p) for p in self.queued_players)
        players_info = "\n".join(str(p) for p in self.players)
        last_updates_info = "\n".join(str(update) for update in self.last_updates)

        return (
            f"ServerStateMessage:\n"
            f"  Client ID: {self.client_id}\n"
            f"  Username: {self.username}\n"
            f"  Game State: {self.game_state if self.game_state else 'None'}\n"
            f"  Hand: {self.hand if self.hand else 'None'}\n"
            f"  In-Game Players:\n{in_game_players_info}\n"
            f"  Spectator Players:\n{spectator_players_info}\n"
            f"  Queued Players:\n{queued_players_info}\n"
            f"  Players:\n{players_info}\n"
            f"  Last Updates:\n{last_updates_info}"
        )
