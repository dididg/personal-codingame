## GA solution

#########################################################################################################################################
## Imports

import sys
import math
import numpy as np

#########################################################################################################################################
## Classes

class Point:
    def __init__(self, x, y):
		self.x = x
		self.y = y
		
	def distance_squared(self, p):
		return (self.x - P.x)**2 + (self.y - p.y)**2
	
	def distance(self, p):
		return np.sqrt(distance_squared(self, p))
	
	def closest(self, pa, pb):
		# Determine the closest point to self on a line containing pa and pb
		da = pb.y - pa.y
		db = a.x - b.x
		c1 = da*a.x + db*a.y
		c2 = -db*self.x + da*self.y
		det = da*da + db*db
		cx = 0
		cy = 0
		
		if det != 0:
			cx = (da*c1 - db*c2) / det
        	cy = (da*c2 + db*c1) / det
		else:
			cx = this.x;
        	cy = this.y;
		return Point(cx, cy)

	
class Unit(Point):
	def __init__(self, id, r, vx, vy):
		super.__init__(self, vx, vy)
		self.id = id
		self.r = r
		
	def collision(self, u):
		# Determine whether self and unit u will collide, and when; returns a Collision type
		# Square of the distance
    	dist = self.distance2(u)
		
    	#Sum of the radii squared
    	sr = (self.r + u.r)*(self.r + u.r);
		
		if dist < sr: # Objects are already touching each other. We have an immediate collision.
			return Collision(self, u, 0.0)
		# Optimisation. Objects with the same speed will never collide
		if self.vx == u.vx and self.vy == u.vy:
			return None
		# in the reference frame of u - u is stationary
		x = self.x - u.x
		y = self.y - u.y
		myp = Point(x, y)
		vx = self.vx - u.vx
		vy = self.vy - u.vy
		up = Point(0, 0)

		# We look for the closest point to u (which is in (0,0)) on the line described by our speed vector
		p = up.closest(myp, Point(x + vx, y + vy))

		# Square of the distance between u and the closest point to u on the line described by our speed vector
		pdist = up.distance2(p)

		# Square of the distance between us and that point
		mypdist = myp.distance2(p)

		# If the distance between u and this line is less than the sum of the radii, there might be a collision
		if pdist < sr:
			# Our speed on the line
			length = np.sqrt(vx*vx + vy*vy)

			# We move along the line to find the point of impact
			backdist = np.sqrt(sr - pdist)
			p.x = p.x - backdist * (vx / length)
			p.y = p.y - backdist * (vy / length)

			# If the point is now further away it means we are not going the right way, therefore the collision won't happen
			if myp.distance2(p) > mypdist:
				return None

			pdist = p.distance(myp)

			# The point of impact is further than what we can travel in one turn
			if pdist > length:
				return None

			# Time needed to reach the impact point
			t = pdist / length

			return Collision(self, u, t)

		return None
		
	def bounce(self, u):
		# if collision between pod and checkpoint : no bounce
		# if collision between pods, bounce (perfect elastic collisions with 120 half-momentum)
		if isinstance(u, Checkpoint):
        	# Collision with a checkpoint
        	self.bounceWithCheckpoint(u)
		else :
			# If a pod has its shield active its mass is 10 otherwise it's 1
			m1 = 10. if this.shield else 1.
			m2 = 10. if u.shield else 1.
			mcoeff = (m1 + m2) / (m1 * m2)

			nx = self.x - u.x
			ny = self.y - u.y

			# Square of the distance between the 2 pods. This value could be hardcoded because it is always 800²
			nxnysquare = nx*nx + ny*ny

			dvx = self.vx - u.vx
			dvy = self.vy - u.vy

			# fx and fy are the components of the impact vector. product is just there for optimisation purposes
			product = nx*dvx + ny*dvy
			fx = (nx * product) / (nxnysquare * mcoeff)
			fy = (ny * product) / (nxnysquare * mcoeff)

			# We apply the impact vector once
			self.vx -= fx / m1
			self.vy -= fy / m1
			u.vx += fx / m2
			u.vy += fy / m2

			# If the norm of the impact vector is less than 120, we normalize it to 120
			impulse = np.sqrt(fx*fx + fy*fy)
			if impulse < 120.0:
				fx = fx * 120.0 / impulse
				fy = fy * 120.0 / impulse
			
			# We apply the impact vector a second time
			self.vx -= fx / m1
			self.vy -= fy / m1
			u.vx += fx / m2
			u.vy += fy / m2

class Checkpoint(Unit):
	def __init__(self, id, vx, vy):
		super.__init__(self, id, R_CHECKPOINT, vx, vy)
				
	def bounce(self, p)
	
class Pod(Unit): 
	def __init__(self, id, x, y, angle, nextCheckpointId, checked, timeout, partner, shield):
		super.__init__(self, id, R_POD, x, y)
		self.angle = angle
		self.nextCheckpointId = nextCheckpointId
		self.checked = checked
		self.timeout = timeout
		self.partner = partner
		self.shield = shield
		self.vx = 0
		self.vy = 0	
		
	def __init__(self, id, x, y, vx, vy, angle, nextCheckpointId, checked, timeout, partner, shield):
		super.__init__(self, id, R_POD, x, y)
		self.angle = angle
		self.nextCheckpointId = nextCheckpointId
		self.checked = checked
		self.timeout = timeout
		self.partner = partner
		self.shield = shield
		self.vx = vx
		self.vy = vy	
		
	def get_angle(self, p):
		d = self.distance(p)
		dx = (p.x - self.x)/d
		dy = (p.y - self.y)/d
		a = np.acos(dx)*180./np.pi()
		#If the point I want is below me, I have to shift the angle for it to be correct
		if dy < 0:
			a = 360. - a
		return a
		
	def diff_angle(self, p):
		right = a - self.angle if self.angle <= a else 360. - self.angle + a
		left = self.angle - a if self.angle >= a else self.angle + 360. - a
		return right if right < left else -left #if we rotate to left we must return a negative angle
		
	def rotate(self, p):
		a = self.diff_angle(p)
		# can't turn by more than 18° in one turn
		if a > 18.:
			a = 18.
		elif a < -18.:
			a = -18.
			
		self.angle += a
		
		if self.angle > 360.:
			self.angle -= 360.
		elif self.angle < 0.:
			self.angle += 360.
		
	def boost(self, thrust):
		# if shield is on, no acceleration for 3 turns
		if self.shield:
			return
		
		# radians
		ra = self.angle*np.pi()/180.
		
		self.vx += cos(ra)*thrust
		self.vy += sin(ra)*thrust
		
	def move(self, t):
		self.x += self.vx * t
		self.y += self.vy * t
		
	def end(self):
		self.x = round(self.x)
		self.y = round(self.y)
		self.vx = int(self.vx * 0.85)
		self.vy = int(self.vy * 0.85)
		self.timeout -= 1
	
	def play(self, p, thrust):
		self.rotate(p)
		self.boost(thrust)
		self.move(1.0)
		self.end()
	
	def bounce(self, u)	
	
	def output(self, move):
	
class Collision:
	def __init__(self, ua, ub, t):
		self.ua = ua
		self.ub = ub
		self.t = t
	
class Solution:
	def __init__(self):
		return
	def randomize(self)
	
class Move:
	def __init__(self):
		return
	def mutate(self, amplitude)

	
	
	

def play(pods, checkpoints):
    # This tracks the time during the turn. The goal is to reach 1.0
    t = 0.0

    while t < 1.0 :
        firstCollision = None

        # We look for all the collisions that are going to occur during the turn
        for int i = 0; i < pods.length; ++i:
            # Collision with another pod?
            for int j = i + 1; j < pods.length; ++j:
                col = pods[i].collision(pods[j])

                # If the collision occurs earlier than the one we currently have we keep it
                if col != null && col.t + t < 1.0 && (firstCollision == null || col.t < firstCollision.t):
                    firstCollision = col

            # Collision with another checkpoint?
            # It is unnecessary to check all checkpoints here. We only test the pod's next checkpoint.
            # We could look for the collisions of the pod with all the checkpoints, but if such a collision happens it wouldn't impact the game in any way
            col = pods[i].collision(checkpoints[pods[i].nextCheckpointId])

            # If the collision happens earlier than the current one we keep it
            if col != null && col.t + t < 1.0 && (firstCollision == null || col.t < firstCollision.t):
                firstCollision = col
            
        if firstCollision == None:
            # No collision, we can move the pods until the end of the turn
            for (int i = 0; i < pods.length; ++i:
                pods[i].move(1.0 - t)
            
            # End of the turn
            t = 1.0
				 
        else:
            # Move the pods to reach the time `t` of the collision
            for int i = 0; i < pods.length; ++i:
                pods[i].move(firstCollision.t)
            
            # Play out the collision
            firstCollision.a.bounce(firstCollision.b)

            t += firstCollision.t
      
    for int i = 0; i < pods.length; ++i:
        pods[i].end()
    





# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

checkpoints = {}
pos = {}
# game loop
while True:
    # next_checkpoint_x: x position of the next check point
    # next_checkpoint_y: y position of the next check point
    # next_checkpoint_dist: distance to the next checkpoint
    # next_checkpoint_angle: angle between your pod orientation and the direction of the next checkpoint
    x, y, next_checkpoint_x, next_checkpoint_y, next_checkpoint_dist, next_checkpoint_angle = [int(i) for i in input().split()]
    opponent_x, opponent_y = [int(i) for i in input().split()]

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)

    
    # You have to output the target position
    # followed by the power (0 <= thrust <= 100)
    # i.e.: "x y thrust"

    # in case of a collision if the opponent is in front of me, colliding is an advantage to me
    # but in case of a collision if the opponent is behind me, colliding is an advantage to them
    



    # print output
    print(answer)
