from sqlalchemy.orm import Session

from app import crud, schemas
from app.db import base  # noqa: F401
import logging

logger = logging.getLogger(__name__)
# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28
from app.models import Bike  # noqa

bikes_data = [
	{
		"id": 1,
		"model_id": 1,
		"color": "Bright Red",
		"required_licence": "2B",
		"transmission": "automatic",
		"storage_box": True,
		"rate": 35,
		"rate_unit": "$",
		"description": "Our Iconic Red Vespa LX150 sporting the famous Italian red color. A symbol of the Vespas that has famously grace many movies. With a 150cc fully automatic engine as well as a back box. You will have a chill time riding it around Singapore. It is a very iconic, functional and nimble bike to ride around!",
		"images": [
			"https://static.wixstatic.com/media/7d3c4e_9099006a2cc44c4698d32ddd131ddc36~mv2.jpg/v1/fill/w_1079,h_565,al_c,q_85/7d3c4e_9099006a2cc44c4698d32ddd131ddc36~mv2.webp",
			"https://static.wixstatic.com/media/7d3c4e_495177dc15dd4b1598f1cc6de6c2084f~mv2.jpg/v1/fill/w_1080,h_969,al_c,q_85/7d3c4e_495177dc15dd4b1598f1cc6de6c2084f~mv2.webp",
		],
	},
	{
		"id": 2,
		"model_id": 1,
		"color": "Black",
		"required_licence": "2B",
		"transmission": "automatic",
		"storage_box": True,
		"rate": 35,
		"rate_unit": "$",
		"description": "Our Black Vespa LX150 are more for the discrete riders who love the look, functionality and ride of a small Vespa. With a 150cc fully automatic engine as well as a back box. You will have a chill time riding it around Singapore. It is a very iconic, functional and nimble bike to ride around!",
		"images": [
			"https://static.wixstatic.com/media/7d3c4e_36b9106303d7479abd088fb00d1eca15~mv2.jpg/v1/fill/w_565,h_565,al_c,q_80/7d3c4e_36b9106303d7479abd088fb00d1eca15~mv2.webp",
			"https://static.wixstatic.com/media/7d3c4e_524897b421c04af7a2f0b7d4121a9891~mv2.jpg/v1/fill/w_922,h_1152,al_c,q_85,usm_0.66_1.00_0.01/7d3c4e_524897b421c04af7a2f0b7d4121a9891~mv2.webp",
		],
	},
	{
		"id": 3,
		"model_id": 1,
		"color": "White",
		"required_licence": "2B",
		"transmission": "automatic",
		"storage_box": True,
		"rate": 35,
		"rate_unit": "$",
		"description": "Our White Vespa LX150 is one that shows off the curves of the Vespa bodystyle in great fashion. With a 150cc fully automatic engine as well as a back box. You will have a chill time riding it around Singapore. It is a very iconic, functional and nimble bike to ride around!",
		"images": [
			"https://static.wixstatic.com/media/7d3c4e_b92c5aa58e3344ccacf6979f3857b560~mv2.jpg/v1/fill/w_1248,h_653,al_c,q_85,usm_0.66_1.00_0.01/7d3c4e_b92c5aa58e3344ccacf6979f3857b560~mv2.webp",
			"https://static.wixstatic.com/media/7d3c4e_0576a342e37040d4bcabb4ce594bd5e6~mv2.jpg/v1/fill/w_1248,h_653,al_c,q_85,usm_0.66_1.00_0.01/7d3c4e_0576a342e37040d4bcabb4ce594bd5e6~mv2.webp",
			"https://static.wixstatic.com/media/7d3c4e_355d4b5a1ee24ef6995acef2b42aa38c~mv2.jpg/v1/fill/w_1248,h_653,al_c,q_85,usm_0.66_1.00_0.01/7d3c4e_355d4b5a1ee24ef6995acef2b42aa38c~mv2.webp",
			"https://static.wixstatic.com/media/7d3c4e_926f5031ac9644b592fb6838ae4de86e~mv2.jpg/v1/fill/w_922,h_1152,al_c,q_85,usm_0.66_1.00_0.01/7d3c4e_926f5031ac9644b592fb6838ae4de86e~mv2.webp",
			"https://static.wixstatic.com/media/7d3c4e_19a87dcbdd6b4a43b36d9cd809b4059a~mv2.jpg/v1/fill/w_1024,h_756,al_c,q_85/7d3c4e_19a87dcbdd6b4a43b36d9cd809b4059a~mv2.webp",
		],
	},
	{
		"id": 4,
		"model_id": 2,
		"color": "Orange",
		"required_licence": "2B",
		"transmission": "manual",
		"storage_box": False,
		"rate": 35,
		"rate_unit": "$",
		"description": "The most powerful class 2B bike available. The KTM engine revs to 10,500rpm and delivers it with torque that no other class 2B bike can. Our KTM Duke 200 is fitted with the best quality tyre (Pirelli Rosso) along with a fully rebuilt engine for best reliability, performance and safety!",
		"images": [
			"https://static.wixstatic.com/media/7d3c4e_db86ae65cc5246e1969455e18124d8bb~mv2.jpg/v1/fill/w_1080,h_565,al_c,q_85/7d3c4e_db86ae65cc5246e1969455e18124d8bb~mv2.webp",
			"https://static.wixstatic.com/media/7d3c4e_ae52dfc49b38499ab9735c3c98144b4c~mv2.jpg/v1/fill/w_1080,h_565,al_c,q_85/7d3c4e_ae52dfc49b38499ab9735c3c98144b4c~mv2.webp",
			"https://static.wixstatic.com/media/7d3c4e_83283255affb4fa2861490b36c4ed775~mv2.jpg/v1/fill/w_922,h_1152,al_c,q_85,usm_0.66_1.00_0.01/7d3c4e_83283255affb4fa2861490b36c4ed775~mv2.webp",
		],
	},
	{
		"id": 5,
		"model_id": 3,
		"color": "Grey",
		"required_licence": "2A",
		"transmission": "automatic",
		"storage_box": False,
		"rate": 40,
		"rate_unit": "$",
		"description": "The biggest and fastest Vespa available. With its 280cc engine, you have the body style of the vespa and the speed to match! A unique shade of grey, we have resprayed it to give it the best look. Now you have the style and the speed with the GTS300 Super.",
		"images": [
			"https://static.wixstatic.com/media/7d3c4e_1c3d73a073914682982fc6fd9f2a00ad~mv2.jpg/v1/fill/w_1248,h_832,al_c,q_85,usm_0.66_1.00_0.01/7d3c4e_1c3d73a073914682982fc6fd9f2a00ad~mv2.webp",
			"https://static.wixstatic.com/media/7d3c4e_e121a272dade4c5c9e9b8a2b348ddf32~mv2.jpg/v1/fill/w_1248,h_832,al_c,q_85,usm_0.66_1.00_0.01/7d3c4e_e121a272dade4c5c9e9b8a2b348ddf32~mv2.webp",
		],
	},
	{
		"id": 6,
		"model_id": 3,
		"color": "Black Modified",
		"required_licence": "2A",
		"transmission": "automatic",
		"storage_box": False,
		"rate": 40,
		"rate_unit": "$",
		"description": "The biggest and fastest Vespa available. With its 280cc engine, you have the body style of the vespa and the speed to match! We have included black Zeloni aftermarket parts (Italian tuning brand) to give the ultimate Vespa look. Now you have the style and the speed with the GTS300 Super.",
		"images": [
			"https://static.wixstatic.com/media/7d3c4e_597f9679b3024a939733dc68f3d307de~mv2.jpg/v1/fill/w_1248,h_832,al_c,q_85,usm_0.66_1.00_0.01/7d3c4e_597f9679b3024a939733dc68f3d307de~mv2.webp",
			"https://static.wixstatic.com/media/7d3c4e_fa8b23f889a147cc80b3e2a9734971ec~mv2.jpg/v1/fill/w_1248,h_832,al_c,q_85,usm_0.66_1.00_0.01/7d3c4e_fa8b23f889a147cc80b3e2a9734971ec~mv2.webp",
		],
	},
	{
		"id": 7,
		"model_id": 4,
		"color": "Orange",
		"required_licence": "2A",
		"transmission": "manual",
		"storage_box": True,
		"rate": 40,
		"rate_unit": "$",
		"description": "A very powerful class 2A bike. The KTM engine is one that revs to 10,500rpm and delivers it with relentless torque. Our KTM Duke 390 is fitted with a back box for functionality along with a rebuilt engine for best reliability, performance and safety!",
		"images": [
			"https://static.wixstatic.com/media/7d3c4e_25c6848d8b104e31bbd360c119f230a3~mv2.jpg/v1/fill/w_1248,h_832,al_c,q_85,usm_0.66_1.00_0.01/7d3c4e_25c6848d8b104e31bbd360c119f230a3~mv2.webp",
			"https://static.wixstatic.com/media/7d3c4e_979e467554a44ae0ab5dccfb7eb75658~mv2.jpg/v1/fill/w_1247,h_833,al_c,q_85,usm_0.66_1.00_0.01/7d3c4e_979e467554a44ae0ab5dccfb7eb75658~mv2.webp",
		],
	},
	{
		"id": 8,
		"model_id": 1,
		"color": "Pastle Green",
		"required_licence": "2B",
		"transmission": "automatic",
		"storage_box": True,
		"rate": 35,
		"rate_unit": "$",
		"description": "Our Pastle Green Vespa LX150 is for those that love the pastle shades and is not afraid of showing it. With a 150cc fully automatic engine as well as a back box. You will have a chill time riding it around Singapore. It is a very iconic, functional and nimble bike to ride around!",
		"images": [
			"https://static.wixstatic.com/media/7d3c4e_953719c2104b471c8b70433806302247~mv2.jpg/v1/fill/w_1248,h_832,al_c,q_85,usm_0.66_1.00_0.01/7d3c4e_953719c2104b471c8b70433806302247~mv2.webp",
			"https://static.wixstatic.com/media/7d3c4e_fb501462092442528e91865e44def532~mv2.jpg/v1/fill/w_1248,h_832,al_c,q_85,usm_0.66_1.00_0.01/7d3c4e_fb501462092442528e91865e44def532~mv2.webp",
		],
	},
	{
		"id": 9,
		"model_id": 1,
		"color": "Navy Blue",
		"required_licence": "2B",
		"transmission": "automatic",
		"storage_box": True,
		"rate": 35,
		"rate_unit": "$",
		"description": "Our Navy Blue Vespa LX150 are more for the discrete riders who love the blue dark look. With a 150cc fully automatic engine as well as a back box. You will have a chill time riding it around Singapore. It is a very iconic, functional and nimble bike to ride around!",
		"images": [
			"https://static.wixstatic.com/media/7d3c4e_1789bc97016549c29e02f1b7807dac31~mv2.jpg/v1/fill/w_1248,h_832,al_c,q_85,usm_0.66_1.00_0.01/7d3c4e_1789bc97016549c29e02f1b7807dac31~mv2.webp",
			"https://static.wixstatic.com/media/7d3c4e_02461206ed344a8fa5f2c490529f8cf8~mv2.jpg/v1/fill/w_1248,h_832,al_c,q_85,usm_0.66_1.00_0.01/7d3c4e_02461206ed344a8fa5f2c490529f8cf8~mv2.webp",
		],
	},
	{
		"id": 10,
		"model_id": 1,
		"color": "Deep Blue",
		"required_licence": "2B",
		"transmission": "automatic",
		"storage_box": True,
		"rate": 35,
		"rate_unit": "$",
		"description": "Our Deep Blue Vespa LX150 are for those who like the modified look of the Vespa. It comes with upgraded Akrapovic exhaust, a front fender change and rebuilt engine. With a 150cc fully automatic engine as well as a back box. You will have a chill time riding it around Singapore. It is a very iconic, functional and nimble bike to ride around!",
		"images": [
			"https://static.wixstatic.com/media/7d3c4e_567483a0c8c1476d95baed7a092c95e6~mv2.jpg/v1/fill/w_1248,h_832,al_c,q_85,usm_0.66_1.00_0.01/7d3c4e_567483a0c8c1476d95baed7a092c95e6~mv2.webp",
			"https://static.wixstatic.com/media/7d3c4e_09364f5f2741496486e1a606123966e5~mv2.jpg/v1/fill/w_1248,h_832,al_c,q_85,usm_0.66_1.00_0.01/7d3c4e_09364f5f2741496486e1a606123966e5~mv2.webp",
		],
	},
	{
		"id": 11,
		"model_id": 5,
		"color": "Black",
		"required_licence": "2B",
		"transmission": "manual",
		"storage_box": False,
		"rate": 30,
		"rate_unit": "$",
		"description": "The black Honda MSX is such a unique and cute bike. However, it has a great little engine that revs to 9,000rpm and makes the journey around town so much more fun with its nimble handling. This is the 2014 model and it wears black fairings to give it a meaner look.",
		"images": [
			"https://static.wixstatic.com/media/7d3c4e_91356a4715a64142911f4b0bf18c57a1~mv2.jpg/v1/fill/w_1248,h_832,al_c,q_85,usm_0.66_1.00_0.01/7d3c4e_91356a4715a64142911f4b0bf18c57a1~mv2.webp",
			"https://static.wixstatic.com/media/7d3c4e_de3f1833e59045098a95dd764061491a~mv2.jpg/v1/fill/w_1248,h_832,al_c,q_85,usm_0.66_1.00_0.01/7d3c4e_de3f1833e59045098a95dd764061491a~mv2.webp",
		],
	},
	{
		"id": 12,
		"model_id": 6,
		"color": "Black",
		"required_licence": "2B",
		"transmission": "manual",
		"storage_box": False,
		"rate": 30,
		"rate_unit": "$",
		"description": "The RXZ is a blast from the past. A classic 2 stroke machine. One that reminds us our the bikes we used to ride in the past as more 2 strokes get sent to the scrapyard. Riding this an analog experience no other modern bike can provide.",
		"images": [
			"https://static.wixstatic.com/media/7d3c4e_d0c8303a11814238a2c623a31dca6dba~mv2.jpg/v1/fill/w_1248,h_832,al_c,q_85,usm_0.66_1.00_0.01/7d3c4e_d0c8303a11814238a2c623a31dca6dba~mv2.webp",
			"https://static.wixstatic.com/media/7d3c4e_542cb123f0d54420b58c8456c0492561~mv2.jpg/v1/fill/w_1248,h_832,al_c,q_85,usm_0.66_1.00_0.01/7d3c4e_542cb123f0d54420b58c8456c0492561~mv2.webp",
		],
	},
]


def initial_bike_data(db: Session) -> None:
	logger.info("Creating initial bike data")
	count = 0
	for bike_data in bikes_data:
		if crud.bike.get(db, id=bike_data.get("id")):
			continue
		bike = schemas.Bike(
			id=bike_data.get("id"),
			model_id=bike_data.get("model_id"),
			color=bike_data.get("color"),
			required_licence=bike_data.get("required_licence"),
			transmission=bike_data.get("transmission"),
			storage_box=bike_data.get("storage_box"),
			rate=bike_data.get("rate"),
			rate_unit=bike_data.get("$"),
			description=bike_data.get("description"),
			images=bike_data.get("images"),
		)
		crud.bike.create(db, obj_in=bike)
		count += 1
	logger.info(f"Created {count} initial bike data")
	db.execute("SELECT setval('bike_id_seq', (SELECT max(id) FROM bike));")
	db.commit()
