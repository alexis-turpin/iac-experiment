# Infrastructure as code experiment

I've made this small project on my short evening and week-ends since mid-November. The goal is refresh my existing
skills and experiment new ones.

For now, it is planned in 3 part :
  - Infrastructure
  - Api (back)
  - Front

## Project content
### Infrastructure

_That's by far the part I wanted to do the most, so much that I have created the 2 others just to allow my
infrastructure to exist._

My goal here is to have an infrastructure as code entirely **reusable**, **highly available** and trying to respect
best practices.

Using: [Terraform](https://www.terraform.io/); [AWS](https://aws.amazon.com/)

More on this part [here](https://github.com/alexis-turpin/iac-experiment/tree/master/infrastructure).

### API

_I've been using Python since a few years now, but mainly for scripting or even
[competitive programming](http://codingame.com/), but not much for bigger projects._

Here the code is fairly simple: a basic Rest API implementing main HTTP methods. Trying to keep the code elegant,
and respect best practices.

Using: [Tornado](http://www.tornadoweb.org/)

More on this part [here](https://github.com/alexis-turpin/iac-experiment/tree/master/api).


### Front

_For me the least interesting part, but it must be done in order to test things out_
```
# TODO
```
The most basic web client to my Rest API, just to test things out. Once the rest will be done I could implement
other things to make it more interesting : Caching, Authentication ...

Using: [Tornado](http://www.tornadoweb.org/)

More on this part [here](https://github.com/alexis-turpin/iac-experiment/tree/master/front). 

## How can you participate ?

Obviously this project having no proper goal except practicing, I'm not expecting you to open and pull request.
But you are very welcome to [open issues](https://github.com/alexis-turpin/iac-experiment/issues/new) to :
  - Point out some mistakes / bugs,
  - Recommend me to implement some missing features,
  - Remind me of some of the Industry's best practices,
  - Or even correct some tiny nits that keep you up at night :) 
