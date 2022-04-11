all: ping

ping:
	@ansible all -i hosts -m ping

delivery:
	@ansible-playbook -i hosts playbook.yml
