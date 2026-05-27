provider "aws" {
  region = "us-east-1"
}

resource "aws_instance" "example" {
  ami           = "ami-020cba7c55df1f615"
  instance_type = "t3.micro"
  subnet_id     = "subnet-0bc3c6c4e673ecb5c"  # Replace with your actual subnet ID

  tags = {
    Name = "ExampleInstance"
  }
}
