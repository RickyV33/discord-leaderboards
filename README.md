# Gooner, The Discord Bot
My friends and I play daily games like Framed and Thrice with some regularity and share our scores on Discord. I've had some curiosity as to what our overall scores look like, so I wrote this bot to keep track of that for us. 

I'm relearning Python for my new job, so this was also an excuse to get some additional practice. I learned some things a long the way, which I'll share in this README.


### My Journey with Python

1. **Holy DI**. Since you can monkey patch in Python, DI seems to have evolved into a hot mess in the Python community (IMO), often favoring quick implementation over more maintainable designs. I tried my hand at actually passing dependencies into class constructors. Doing that manually was pretty annoying, and that led me to explore some DI packages that I'm hoping to use in future projects. 
2. **ORM + API + Business Logic domain? Oh, you mean a DB Model?** This is more applicable to my current job, but the nature of Python development makes it seem prevalent. It seems as though Peewee models (or Django models, at that) get treated as the domain model that drives communication between services. It's _also_ used as the DB api in various services, without leveraging an intermediary db api that manages mapping db modles to business models. On paper that seems fine, but in practice, that can lead to some pretty wild coupling between your database model (read: _how_ you save data) and your business domain (read: _what_ you are doing). Those don't need to be 1-to-1, and for the purpose of extending your application, be it changing how you store data, how you access data, and how your services talk to each other, it often makes sense to have the ORM, db api, and domain models be separate, even if that introduces some redundancy in what you write (hey, with Copilot, that's hardly an excuse these days).
3. With all that said, I fell into some traps in this project. The first of which was passing db models (as the db api) as dependencies when they also act as a a reference to a db object. The second of which was not introducing a DI package sooner.
4. My last note, and I think this is important, is that I'm coming from the JVM. The JVM is such an opinionated ecosystem and the design principles from that ecosystem are really baked into me. I can see those design principles relaxed in Python -- not because you should, but because you can. You can do a hell of a lot more a hell of a lot faster in Python, and I'll be trying my best to embrace some of the nice-to-haves in this language while trying to supoprt some design principles engrained in me, but that might look like me trying to bring the JVM into Python, which doesnt make sense, but might happen. I'm open to learning when it makes sense to do that and when it doesn't. So far, I really like Python. Does it set you up to make some really bad design decisions in the beginning? Absolutely. Will that show up in how you write mocks in tests? Oh brother, you betcha. But all of that _seems_ like it can be avoided with a little bit of engineering experience, so off I go. 
