qt = 44

ele = []

while ele.size != qt/2
	e = rand(1..qt)
	ele << e unless ele.include? e
end

puts ele

User.where(id: ele).each do |user|
  user.is_guest = false
  user.save
end

User.where(is_guest: nil).each do |user|
  user.is_guest = true
  user.save
end
