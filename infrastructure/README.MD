# Infrastructure
_That's by far the part I wanted to do the most, so much that I have created
the 2 others just to allow my infrastructure to exist._

My goal here is to have an infrastructure as code entirely **reusable**,
**highly available** and trying to respect best practices.

Using: [Terraform](https://www.terraform.io/); [AWS](https://aws.amazon.com/)

## Content

The goal is to arrive to this infrastructure for now. More feature might be
added later (DNS, HTTPS, Monitoring...).
![iac_nosg](https://cloud.githubusercontent.com/assets/11937491/20638886/aef990a0-b3ee-11e6-8f4a-47e988bb9503.jpg)

### Modules
I've decided to keep the infrastructure code as [DRY](https://en.wikipedia.org/wiki/Don't_repeat_yourself)
as possible, and as flexible as possible to add features in the future. For
this reason I've created 3 modules :

#### Network
The network module contains not only the network but the whole "static" layout
needed to deploy the rest of the infrastructure. By static I mean the things
that won't be changed much over the time (Subnets, Bastion host ...)

More info about this module [here](modules/network)

#### Data
The data module will define the data layer of my infrastructure. For now it
just represents one RDS server

More info about this module [here](modules/data)

#### Web_infra

As we can see the frontend and backend infrastructure are very similar and, to
respect the DRY principle, they could be created as one module taking different
variables to specialize itself either into frontend or backend.

More info about this module [here](modules/web_infra)
