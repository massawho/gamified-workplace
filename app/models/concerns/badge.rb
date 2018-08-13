module Concerns
  module Badge

    PLATINUM = 4
    GOLD = 3
    SILVER = 2
    BRONZE = 1

    LEVELS = [
      ['Platinum', Badge::PLATINUM],
      ['Gold', Badge::GOLD],
      ['Silver', Badge::SILVER],
      ['Bronze', Badge::BRONZE],
    ]

    def readable_level
      Badge::LEVELS.each do |l|
        return l[0] if l[1] === self.level
      end
    end
  end
end
