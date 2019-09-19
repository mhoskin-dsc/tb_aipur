# -*- coding: utf-8 -*-
"""
Created on Thu Feb 28 08:58:05 2019

@author: hoskim1
"""
from random import shuffle #for deck shuffling
import numpy as np #for random numbers
import time #for delays
from collections import Counter #for dictionary of counts of unique items in list

class Token():
  type = ""
  value = 0
  
  def __init__(self, token_type, value = 0):
    self.type = token_type
    self.value = value
    
  def set_value(self, value):
    self.value = value
    
  def get_type(self):
    return self.type
  
  def get_value(self):
    return self.value


class player():
    
  score = 0
  hidden_score = 0
  camels = 0
  hand = []
    
  def __init__(self, hand = [], score = 0, hidden_score = 0, camels = 0):
      self.hand = hand
      self.score = score
      self.hidden_score = hidden_score
      self.camels = camels

class jp_logic():
    
    delay_time = 1
    
    
    def deck_setup(self):
      c_type = {}
      c_type['r'] = 'Ruby'
      c_type['s'] = 'Silver'
      c_type['g'] = 'Gold'
      c_type['l'] = 'Leather'
      c_type['c'] = 'Cloth'
      c_type['sp'] = 'Spice'
      c_type['cm'] = 'Camel'
      
      c_count = {}
      c_count['r'] = 6
      c_count['s'] = 6
      c_count['g'] = 6
      c_count['l'] = 10
      c_count['c'] = 8
      c_count['sp'] = 8
      c_count['cm'] = 8
      
      deck = []
      
      for c in c_count.keys():
        for n in range(c_count[c]):
          deck.append(c_type[c])
      
      if len(deck) != 52:
        raise ValueError('Length of initial deck incorrect')
      shuffle(deck)
      
      deck = ['Camel','Camel','Camel'] + deck
      
      if len(deck) != 55:
        raise ValueError('Length of shuffled, camelled deck incorrect')
        
      self.deck = deck
    
    
    def token_setup(self):
      
      t_struct = {}
      t_struct['Ruby'] = [7,7,5,5,5]
      t_struct['Silver'] = [5,5,5,5,5]
      t_struct['Gold'] = [6,6,5,5,5]
      t_struct['Leather'] = [4,3,2,1,1,1,1,1,1]
      t_struct['Cloth'] = [4,3,2,2,1,1,1]
      t_struct['Spice'] = [4,4,3,2,1,1,1]
      
      t_struct['Three'] = [1,1,1,2,2,3,3]
      shuffle(t_struct['Three'])
      
      t_struct['Four'] = [4,4,5,5,6,6]
      shuffle(t_struct['Four'])
      
      t_struct['Five'] = [8,8,9,10,10]
      shuffle(t_struct['Five'])
      
      self.tokens = t_struct
      
    def end_game(self):
        self.in_progress = False 
        
        
    def _replace_card(self):
      
      if len(self.deck) == 0:
        print('Deck is empty. Can\'t replace. End of Game.')
        self.end_game()
        
      new_card = self.deck[0]
      print('Replacement Field Card: ', new_card)
      
      self.deck.pop(0)
      self.field.append(new_card)
      

      
      
    def take_card(self, card_idx):
      
      card_chosen = self.field[card_idx]
      self.field.pop(card_idx)
      
      self._replace_card()
     
      self._add_card_to_hand(card_chosen)
      
      
    def _get_camel_count(self, card_list):
      camels = [f for f in card_list if f in ['Camel']]
      return len(camels)
    
    def take_camels(self):
      
      reduced_field = [f for f in self.field if f not in ['Camel']]
      
      num_camels = self._get_camel_count(self.field)
      
      print('Taken', num_camels,'camels')
      self.players[self.player_idx].camels += num_camels
      print('Player', self.player_idx + 1, 'now has', self.players[self.player_idx].camels, 'camels')
      
      self.field = reduced_field
      for i in range(num_camels):
        self._replace_card()
    
      if len(self.field) != 5:
        raise ValueError('Incorrect size of field - though is deck empty??')
          
      pass
    
    
    def _add_card_to_hand(self, card_chosen): 
      self.players[self.player_idx].hand.append(card_chosen)
         
    
    def _add_cards_to_hand(self, cards_chosen):
      for item in cards_chosen:
        self.players[self.player_idx].hand.append(item)
        
    
    
    def swap_with_hand(self, player_hand, field, hand_indexes, field_indexes, camel_count):
      
      cards_to_drop = [player_hand[i] for i in hand_indexes]
      camels_to_drop = ['Camel'] * camel_count
      
      cards_to_drop = cards_to_drop + camels_to_drop
      
      cards_to_take = [field[i] for i in field_indexes]
      
      player_hand = _add_cards_to_hand(player_hand, cards_to_take)
      
    def hand_in_cards(self, card, hand_counter):
      
      #if card in special (global list) quit out
      #else, pop points and add on
      #if num cards 3, 4, 5, do extra add to secret points

      
      
      pass
    
    
    def start(self):
      print('Begin')
      
      self.in_progress = True 
      
      self.player_idx = np.random.randint(2) # 0, 1
      
      print('Player', self.player_idx+1, 'starts')
      self.turn_idx = 1
      while(self.in_progress):
         
        self.turn()
        
        if (self.in_progress):
          t = input('\n\nEnd turn?')
        self.player_idx = 1 - self.player_idx #0 to 1, 1 to 0 
        self.turn_idx += 1
      
      self.assess_winner()
      
      replay = input('Play again y/n')
      if (replay == 'y'):
        g = jp_logic()
        g.start()
     
        
    def assess_winner(self):
      score = [self.players[0].score + self.players[0].hidden_score, 
               self.players[1].score + self.players[1].hidden_score]
      
      if (score[0] == score[1]):
        print('Its a draw! Both players scored ', score[0])
      else:
          
        winning_score = max(score)
        losing_score = min(score)
        winner = score.index(winning_score) + 1
        loser = score.index(losing_score) + 1
        print('Player ', winner, 'won with a score of ', winning_score)
        print('Player ', loser, 'lost with a score of ', losing_score)        
        
        
    def print_summary(self):
        
        print('\n\n')
        print('ROUND: \t', self.turn_idx, '\n')

        print('Player 1: Hand Size:', len(self.players[0].hand), '\t Camel Count:', self.players[0].camels)
        
        print('Player 2: Hand Size:', len(self.players[1].hand), '\t Camel Count:', self.players[1].camels)
      
        print('Cards remaining in Deck:', len(self.deck))
        
        time.sleep(self.delay_time)
        
        print('Tokens:')
        for token_name, token_list in self.tokens.items():
          if token_name not in ['Three','Four','Five']:
            print('\t',token_name, 'Count:', len(token_list), '. Values:', token_list)
          else:
            print('\t',token_name, 'Count:', len(token_list))
        
        print('Field:')
        for card in self.field:
          print('\t', card)    
          
          
        time.sleep(self.delay_time)
        print('Your Hand:')
        print(self.players[self.player_idx].hand)
        print('Your Camels:', self.players[self.player_idx].camels)
        
    def turn(self):
      
      self.print_summary()
      
      option = input('\nChoose an option. \n\t1: Take Camels. \n\t2: Take Card. \n\t3: Swap Cards. \n\t4: Submit Cards\n\t')
      
      if (option == '1'):
        self._camel()
      elif (option == '2'):
        self._take()
      elif (option == '3'):
        self._swap()
      elif (option == '4'):
        self._submit()
      elif (option == '999'):
        self.end_game()
      else:
        print('Unknown value. Please enter a number between 1 and 4.')
        self.turn()
        
        
    
    def _take(self):
      print('take_card')
      
      if (self._get_camel_count(self.field) == 5):
          print('Only Camels available. Choose Option 1 - Take Camels')
          self.turn()
      else:
        for idx, c in enumerate(self.field):
            print(idx + 1, ':', c)
        idx = input('\n Choose a Card Index\n')
      
        #Check if card is a camel
        if (self.field[int(idx) - 1] != 'Camel'):
          self.take_card(int(idx) - 1)
        else:
          print('Invalid option - you can\'t take a single camel!')
          self._take()
      
    def _camel(self):
      print('take_camel')
      
      if (self._get_camel_count(self.field) > 0):
        print('No Camels available. Choose again')
        self.turn()
      else:
        self.take_camels()
        
    def _swap(self):
      print('swap_cards')
        
    def _submit(self):
      print('submit_cards') 
      
      #TODO make a dictionary with a count of cards for printing purposes
            
      hand_details = Counter(self.players[self.player_idx].hand)

      for idx, c in enumerate(list(hand_details.keys())):
        print(idx + 1, ':', c, '(', hand_details[c],' cards)')
      idx = input('\n Choose a Card Index\n')
        
      idx = int(idx) - 1
      if(idx in [l for l in range(len(hand_details))]):
        print('handing in', list(hand_details.keys())[idx])
        self.hand_in_cards(list(hand_details.keys())[idx], hand_details) #TODO, do this
      else:
        print('Invalid option - please specify an integer between 1 and', len(hand_details))
        self._submit()
      
    def __init__(self):
        
      self.deck_setup()
      self.token_setup()
            
      self.field = []
      
      self.players = [player([],0,0,0), player([],0,0,0)]
            
    #  print(len(deck),deck)
      
    #take first 5 and set field
      self.field = self.deck[0:5]
      self.deck = self.deck[5:len(self.deck)+1]
      
      for c in range(0,5):
        #player 1
        if(self.deck[0] != 'Camel'):
          self.players[0].hand.append(self.deck[0])
          self.deck.pop(0)
        else:
          self.players[0].camels += 1
          self.deck.pop(0)
          
        #player 2  
        if(self.deck[0] != 'Camel'):
          self.players[1].hand.append(self.deck[0])
          self.deck.pop(0)
        else:
          self.players[1].camels += 1
          self.deck.pop(0)  
          
      self.players[0].hand.sort()
      self.players[1].hand.sort()
          
      print('Initial Field:', self.field)
      print('P1 Hand:', len(self.players[0].hand), self.players[0].hand, 'P1 Camels:', self.players[0].camels)
      print('P2 Hand:', len(self.players[1].hand), self.players[1].hand, 'P2 Camels:', self.players[1].camels)
  
#  print(len(deck), deck)
  
g = jp_logic()
g.start()